import argparse

def train_model(args):
    # Implement your train model logic here
    print(f"Training model {args.model} with training data {args.train_data}")

def main():
    parser = argparse.ArgumentParser(prog='laiss-lmt', description='Laiss LMT CLI program')
    subparsers = parser.add_subparsers(dest='command')

    train_parser = subparsers.add_parser('train-model', help='Train a model')
    train_parser.add_argument('model', help='Name of the model')
    train_parser.add_argument('--train-data', help='Path to the training data')

    args = parser.parse_args()
    if args.command == 'train-model':
        train_model(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()
