import sys
import argparse
from . import generate, utils, train, build_rag, eval

def main():
    parser = argparse.ArgumentParser(description="RAFT LLM CLI")
    parser.add_argument('command', choices=['generate', 'format', 'train', 'build_rag', 'eval'],
                        help="Subcommand to run")
    
    args = parser.parse_args(sys.argv[1:2])  # Only parse the first argument

    if args.command == 'generate':
        generate.main(sys.argv[2:])
    elif args.command == 'format':
        utils.format.main(sys.argv[2:])
    elif args.command == 'train':
        train.main(sys.argv[2:])
    elif args.command == 'build_rag':
        build_rag.main(sys.argv[2:])
    elif args.command == 'eval':
        eval.main(sys.argv[2:])
    else:
        print("Unknown command")
        sys.exit(1)

if __name__ == "__main__":
    main()