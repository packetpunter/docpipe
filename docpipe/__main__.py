from .docpipe import DocPipe
import fire

def main():
    fire.Fire(DocPipe, name="DocPipe")

if __name__ == "__main__":
    main()