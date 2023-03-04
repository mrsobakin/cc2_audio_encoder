import argparse

from cc2_audio_encoder import bnsf, hca


def cmd_hca(args):
    # TODO: there is probably a better way to do this.
    if args.t and args.k1 and args.k2:
        encryption = {"t": args.t, "k1": args.k1, "k2": args.k2}
    elif args.t or args.k1 or args.k2:
        print("hca encryption key consists of -t, -k1 and -k2 (you should use all of them)")
        exit()
    else:
        encryption = None

    hca_bytes = hca.encode(args.file_in, encryption)
    
    with open(args.file_out, "wb") as f:
        f.write(hca_bytes)


def cmd_bnsf(args):
    if args.stereo:
        encode = bnsf.encode_stereo
    else:
        encode = bnsf.encode_mono

    if args.loop or args.loop_start or args.loop_end:
        loop_info = {"start": args.loop_start, "end": args.loop_end}
    else:
        loop_info = None

    bnsf_bytes = encode(args.file_in, loop_info)

    with open(args.file_out, "wb") as f:
        f.write(bnsf_bytes)


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers(prog="python3 -m cc2_audio_encoder")

    parser_hca = subparsers.add_parser("hca", description="HCA audio encoder + encryptor")
    parser_hca.add_argument("-t", help="Encryption type", type=str)
    parser_hca.add_argument("-k1", help="Key part 1", type=str)
    parser_hca.add_argument("-k2", help="Key part 2", type=str)
    parser_hca.set_defaults(func=cmd_hca)

    parser_bnsf = subparsers.add_parser("bnsf", description="BNSF audio encoder")
    parser_bnsf.add_argument("--stereo", help="Encode as a stereo", action="store_true")
    parser_bnsf.add_argument("--loop", help="Include loop info to the bnsf", action="store_true")
    parser_bnsf.add_argument("--loop-start", help="Start of the loop (In samples). Default is 0. Implies --loop")
    parser_bnsf.add_argument("--loop-end", help="End of the loop (In samples). Default is the last audio sample. Implies --loop")
    parser_bnsf.set_defaults(func=cmd_bnsf)

    parser.add_argument("file_in", type=str)
    parser.add_argument("file_out", type=str)

    args = parser.parse_args()
    if hasattr(args, "func"):
        args.func(args)


main()
