import argparse
import subprocess
import tempfile
import os
import re


def run_command(command):
    """Utility function to run a shell command."""
    try:
        result = subprocess.run(command, check=True, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        return result.stdout, result.stderr
    except subprocess.CalledProcessError as e:
        print(f"Error executing {command}: {e.stderr}")
        exit(1)

def run_mq_command(mq_command):
    """Run an MQ command in a shell script with the MQ environment set up."""
    script_content = f"""
    #!/bin/bash
    . /opt/mqm/bin/setmqenv -s
    export MQSERVER='DEV.APP.SVRCONN/TCP/localhost(1414)'
    export MQSAMP_USER_ID='app'
    {mq_command}
    """
    with tempfile.NamedTemporaryFile(delete=False, mode='w', suffix='.sh') as script_file:
        script_file.write(script_content)
        script_file_path = script_file.name
    os.chmod(script_file_path, 0o755)
    print(f"Running script:\n{script_content}")  # Debugging information
    try:
        output, error = run_command(f"/bin/bash {script_file_path}")
    finally:
        os.remove(script_file_path)
    return output, error

def list_queue_managers(args):
    """List all queue managers."""
    output, error = run_mq_command("dspmq")
    print(output)
    if error:
        print(f"Error: {error}")

def create_queue_manager(args):
    """Create a new queue manager."""
    output, error = run_mq_command(f"/opt/mqm/bin/crtmqm {args.name} && /opt/mqm/bin/strmqm {args.name}")
    print(f"Queue manager {args.name} created and started.\n{output}")
    if error:
        print(f"Error: {error}")

def create_queue(args):
    """Create a queue in the specified queue manager."""
    mqsc_commands = f"""
    DEFINE QLOCAL('{args.queue_name}') REPLACE
    """
    output, error = run_mq_command(f'echo "{mqsc_commands}" | runmqsc {args.qm_name}')
    print(f"Queue {args.queue_name} created in queue manager {args.qm_name}.\n{output}")
    if error:
        print(f"Error: {error}")

def configure_queue(args):
    """Configure an existing queue in the specified queue manager."""
    mqsc_commands = f"""
    ALTER QLOCAL('{args.queue_name}') {args.configuration}
    """
    output, error = run_mq_command(f'echo "{mqsc_commands}" | runmqsc {args.qm_name}')
    print(f"Queue {args.queue_name} configured in queue manager {args.qm_name} with {args.configuration}.\n{output}")
    if error:
        print(f"Error: {error}")

def start_queue_manager(args):
    """Start a queue manager."""
    output, error = run_mq_command(f"/opt/mqm/bin/strmqm {args.name}")
    print(f"Queue manager {args.name} started.\n{output}")
    if error:
        print(f"Error: {error}")

def stop_queue_manager(args):
    """Stop a queue manager."""
    output, error = run_mq_command(f"/opt/mqm/bin/endmqm -i {args.name}")
    print(f"Queue manager {args.name} stopped.\n{output}")
    if error:
        print(f"Error: {error}")

def extract_queue_names(output):
    """Extract queue names from the DISPLAY QUEUE output."""
    queue_name_pattern = re.compile(r"^\s*QUEUE\(([^)]+)\)", re.MULTILINE)
    return [name for name in queue_name_pattern.findall(output) if name != '*']

def display_queues(args):
    """Display all queues in the specified queue manager."""
    command = f'echo "DISPLAY QUEUE(*)" | /opt/mqm/bin/runmqsc {args.qm_name}'
    output, error = run_command(command)
    print(output)
    queue_names = extract_queue_names(output)
    for queue_name in queue_names:
        print(queue_name)

def get_queue_permissions(args):
    """Get permissions for a specific user on all queues in the specified queue manager."""
    queue_manager = args.qm_name
    user = args.user
    command = f'echo "DISPLAY QUEUE(*)" | /opt/mqm/bin/runmqsc {queue_manager}'
    queues_output, _ = run_command(command)
    queue_names = extract_queue_names(queues_output)

    for queue_name in queue_names:
        try:
            command = f'/opt/mqm/bin/dspmqaut -m {queue_manager} -t q -n "{queue_name}" -p {user}'
            permissions_output, error = run_command(command)
            print(f"Permissions for queue '{queue_name}':\n{permissions_output}\n")
            if error:
                print(f"Error: {error}")
        except RuntimeError as e:
            print(f"Error fetching permissions for queue '{queue_name}': {e}")

def put_message(args):
    """Put a message on the specified queue in the specified queue manager."""
    print(f"Enter messages for queue {args.queue_name} (type 'exit' to finish):")

    process = subprocess.Popen(
        f"""/bin/bash -c '
        . /opt/mqm/bin/setmqenv -s
        export MQSERVER="DEV.APP.SVRCONN/TCP/localhost(1414)"
        export MQSAMP_USER_ID="app"
        /opt/mqm/samp/bin/amqsputc {args.queue_name} {args.qm_name}'
        """,
        shell=True,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )

    try:
        while True:
            message = input()
            if message == "exit":
                break
            process.stdin.write(message + "\n")
            process.stdin.flush()
    except BrokenPipeError:
        print("Broken pipe error occurred while writing messages.")
    finally:
        try:
            if process.stdin:
                process.stdin.close()
        except BrokenPipeError:
            pass
        output, error = process.communicate()
        if error:
            print(f"Error: {error}")
        else:
            print(f"Output: {output}")





def get_message(args):
    """Get a message from the specified queue."""
    mq_command = f"/opt/mqm/samp/bin/amqsgetc {args.queue_name} {args.qm_name}"
    output, error = run_mq_command(mq_command)
    print(output)
    if error:
        print(f"Error: {error}")

def main():
    parser = argparse.ArgumentParser(description="IBM MQ Management CLI")
    subparsers = parser.add_subparsers(
        title="subcommands", description="valid subcommands", help="additional help"
    )

    # Subparser for listing queue managers
    parser_list = subparsers.add_parser("list_qm", help="List all queue managers")
    parser_list.set_defaults(func=list_queue_managers)

    # Subparser for creating a queue manager
    parser_create_qm = subparsers.add_parser("create_qm", help="Create a new queue manager")
    parser_create_qm.add_argument("name", help="Name of the queue manager to create")
    parser_create_qm.set_defaults(func=create_queue_manager)
    parser_create_qm.epilog = """
    Example usage:
    ibm-mq-cli create_qm QM1
    ibm-mq-cli create_qm MyQueueManager
    """

    # Subparser for creating a queue
    parser_create_queue = subparsers.add_parser("create_queue", help="Create a queue")
    parser_create_queue.add_argument("qm_name", help="Name of the queue manager")
    parser_create_queue.add_argument("queue_name", help="Name of the queue to create")
    parser_create_queue.set_defaults(func=create_queue)
    parser_create_queue.epilog = """
    Example usage:
    ibm-mq-cli create_queue QM1 DEV.QUEUE.1
    ibm-mq-cli create_queue MyQueueManager MyQueue
    """

    # Subparser for configuring a queue
    parser_configure_queue = subparsers.add_parser("configure_queue", help="Configure a queue")
    parser_configure_queue.add_argument("qm_name", help="Name of the queue manager")
    parser_configure_queue.add_argument("queue_name", help="Name of the queue to configure")
    parser_configure_queue.add_argument("configuration", help="Configuration string for the queue")
    parser_configure_queue.set_defaults(func=configure_queue)
    parser_configure_queue.epilog = """
    Example usage:
    ibm-mq-cli configure_queue QM1 DEV.QUEUE.1 "MAXDEPTH(5000)"
    ibm-mq-cli configure_queue MyQueueManager MyQueue "MAXMSGL(104857600)"
    """

    # Subparser for starting a queue manager
    parser_start_qm = subparsers.add_parser("start_qm", help="Start a queue manager")
    parser_start_qm.add_argument("name", help="Name of the queue manager to start")
    parser_start_qm.set_defaults(func=start_queue_manager)
    parser_start_qm.epilog = """
    Example usage:
    ibm-mq-cli start_qm QM1
    ibm-mq-cli start_qm MyQueueManager
    """

    # Subparser for stopping a queue manager
    parser_stop_qm = subparsers.add_parser("stop_qm", help="Stop a queue manager")
    parser_stop_qm.add_argument("name", help="Name of the queue manager to stop")
    parser_stop_qm.set_defaults(func=stop_queue_manager)
    parser_stop_qm.epilog = """
    Example usage:
    ibm-mq-cli stop_qm QM1
    ibm-mq-cli stop_qm MyQueueManager
    """

    # Subparser for displaying queues
    parser_display_queues = subparsers.add_parser("display_queues", help="Display all queues in a queue manager")
    parser_display_queues.add_argument("qm_name", help="Name of the queue manager")
    parser_display_queues.set_defaults(func=display_queues)
    parser_display_queues.epilog = """
    Example usage:
    ibm-mq-cli display_queues QM1
    ibm-mq-cli display_queues MyQueueManager
    """

    # Subparser for getting queue permissions
    parser_get_permissions = subparsers.add_parser("get_permissions", help="Get permissions for a user on all queues in a queue manager")
    parser_get_permissions.add_argument("qm_name", help="Name of the queue manager")
    parser_get_permissions.add_argument("user", help="Name of the user")
    parser_get_permissions.set_defaults(func=get_queue_permissions)
    parser_get_permissions.epilog = """
    Example usage:
    ibm-mq-cli get_permissions QM1 myuser
    ibm-mq-cli get_permissions MyQueueManager anotheruser
    """

    # Subparser for putting a message on a queue
    parser_put_message = subparsers.add_parser("put_message", help="Put a message on a queue")
    parser_put_message.add_argument("queue_name", help="Name of the queue")
    parser_put_message.add_argument("qm_name", help="Name of the queue manager")
    parser_put_message.set_defaults(func=put_message)
    parser_put_message.epilog = """
    Example usage:
    ibm-mq-cli put_message DEV.QUEUE.1 QM1
    """

    # Subparser for getting a message from a queue
    parser_get_message = subparsers.add_parser("get_message", help="Get a message from a queue")
    parser_get_message.add_argument("queue_name", help="Name of the queue")
    parser_get_message.add_argument("qm_name", help="Name of the queue manager")
    parser_get_message.set_defaults(func=get_message)
    parser_get_message.epilog = """
    Example usage:
    ibm-mq-cli get_message DEV.QUEUE.1 QM1
    """

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
