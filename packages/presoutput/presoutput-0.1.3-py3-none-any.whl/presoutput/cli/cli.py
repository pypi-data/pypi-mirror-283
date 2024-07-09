from ..quarto_output import qmd_to_pdf, qmd_to_pptx

import argparse


def _cli():
    """
    Function for running qmd_to_pdf or qmd_to_pptx via command line.
    Use either of the above functions instead if running via a python script.
    """

    parser = argparse.ArgumentParser(
        description="Create a PDF or PPTX from your quarto template."
    )

    parser.add_argument("input", type=str, help="The input QMD file name")
    parser.add_argument(
        "-t",
        "--type",
        type=str,
        default="pdf",
        help="The output type (pdf or pptx). (optional, defaults to pdf)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default=None,
        help="The output PDF/PPTX filename (optional)",
    )
    parser.add_argument(
        "-di",
        "--delete_intermediates",
        action="store_false",
        help="Do not delete intermediate files if included (optional)",
    )
    parser.add_argument(
        "-b",
        "--browser",
        type=str,
        default=None,
        help="Specify the browser to use (optional)",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=300,
        help="DPI for the PPTX slides (optional, defaults to 300)",
    )
    parser.add_argument(
        "-ph",
        "--pptx_height",
        type=float,
        default=7.5,
        help="Height of the PPTX slide in inches (optional, defaults to 7.5)",
    )
    parser.add_argument(
        "-pw",
        "--pptx_width",
        type=float,
        default=13.33,
        help="Width of the PPTX slide in inches (optional, defaults to 13.33)",
    )
    parser.add_argument(
        "-v", "--verbose", type=int, default=0, help="Verbose level (optional)"
    )

    args = parser.parse_args()

    if args.type.lower() == "pptx":
        qmd_to_pptx(
            input_filename=args.input,
            output_filename=args.output,
            delete_intermediate=args.delete_intermediates,
            dpi=args.dpi,
            pptx_height=args.pptx_height,
            pptx_width=args.pptx_width,
            browser=args.browser,
            verbose=args.verbose,
        )
    else:
        qmd_to_pdf(
            input_filename=args.input,
            output_filename=args.output,
            delete_intermediate=args.delete_intermediates,
            browser=args.browser,
            verbose=args.verbose,
        )


if __name__ == "__main__":
    _cli()
