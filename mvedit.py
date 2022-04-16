#!/usr/bin/env python3
import argparse
import os
import shlex
import subprocess
import sys
import tempfile

def launch_editor(edit_command, initial_content):
    with tempfile.NamedTemporaryFile(mode="w+") as tf:
        tf.write(initial_content)
        tf.flush()

        subprocess.run(shlex.split(edit_command) + [tf.name])

        tf.seek(0)
        return tf.read()

def prompt(prompt_str, options):
    assert len(options) == len(set(o[0] for o in options)), "Options not unique"
    options_str = ", ".join(f"({o[0]}){o[1:]}" for o in options)
    while True:
        sys.stdout.write(f"{prompt_str} [{options_str}]: ")
        s = input().lower()
        if s:
            matching = [o for o in options if o.startswith(s)]
            if len(matching) > 0:
                assert len(matching) == 1
                return matching[0]
            else:
                print("Invalid input")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--edit-command", "-e", default=os.environ.get("EDITOR", "vim"))
    parser.add_argument("--move-command", "-m", default=os.environ.get("MOVE", "mv"))
    parser.add_argument("--remove-command", "-r", default=os.environ.get("REMOVE", "rm"))
    parser.add_argument("--yes", "-y")
    parser.add_argument("files", nargs="+")
    args = parser.parse_args()

    for fname in args.files:
        if not os.path.isfile(fname):
            sys.exit(f"'{fname}' does not exist")

    editor_content = "\n".join(args.files)
    while True:
        try:
            editor_content = launch_editor(args.edit_command, editor_content)
        except subprocess.CalledProcessError as exc:
            sys.exit(str(exc))

        edited_files = editor_content.split("\n")
        if len(args.files) != len(edited_files):
            resp = prompt("Number of lines has changed. Edit again?", ["yes", "no"])
            if resp == "no":
                sys.exit(0)
        else:
            edits = [(args.files[i], edited_files[i]) for i in range(len(args.files)) if args.files[i] != edited_files[i]]
            if len(edits) == 0:
                print("No changes")
                sys.exit(0)
            for src, dst in edits:
                dst_rm = dst
                if len(dst_rm) == 0:
                    dst_rm = "<removed>"
                print(f"{src} -> {dst_rm}")
            resp = prompt("Execute operations?", ["yes", "no", "edit"])
            if resp == "no":
                sys.exit("Aborted.")
            elif resp == "yes":
                try:
                    for src, dst in edits:
                        if len(dst) == 0:
                            subprocess.run(shlex.split(args.remove_command) + [src])
                        else:
                            subprocess.run(shlex.split(args.move_command) + [src, dst])
                except subprocess.CalledProcessError as exc:
                    sys.exit(str(exc))
                break


if __name__ == "__main__":
    main()