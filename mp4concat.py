"""
This is a script that losslessly concatenates MP4 files (H.264 video and AAC audio) 
by first transcoding them to MPEG-2 transport streams as documented at
https://trac.ffmpeg.org/wiki/Concatenate, i.e. it does the equivalent of
    ffmpeg -i input1.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate1.ts
    ffmpeg -i input2.mp4 -c copy -bsf:v h264_mp4toannexb -f mpegts intermediate2.ts
    ffmpeg -i "concat:intermediate1.ts|intermediate2.ts" -c copy -bsf:a aac_adtstoasc output.mp4

To run this script, execute
    python mp4concat input1.mp4 input2.mp4 ... --output output.mp4
in a Python environment in which 'click' is installed (execute 'pip install click' otherwise)

MIT License
-----------

Copyright (c) 2022 Marc Wouts

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import subprocess
import tempfile

import click


@click.command()
@click.argument("inputs", nargs=-1)
@click.option("--output", nargs=1, help="The result of the concatenation")
def mp4concat(inputs, output):
    """Concatenate MP4 files into a MP4 file without re-encoding"""
    assert output.lower().endswith(
        ".mp4"
    ), f"The destination file {output} should have a .mp4 extension"

    intermediate_ts_files = [tempfile.mktemp() for i in inputs]
    for input_file, intermediate_ts_file in zip(inputs, intermediate_ts_files):
        assert input_file.lower().endswith(
            ".mp4"
        ), f"The input file {output} should have a .mp4 extension"
        process = subprocess.Popen(
            [
                "ffmpeg",
                "-i",
                input_file,
                "-c",
                "copy",
                "-bsf:v",
                "h264_mp4toannexb",
                "-f",
                "mpegts",
                intermediate_ts_file,
            ]
        )
        process.communicate()

    process = subprocess.Popen(
        [
            "ffmpeg",
            "-i",
            "concat:" + "|".join(intermediate_ts_files),
            "-c",
            "copy",
            "-bsf:a",
            "aac_adtstoasc",
            output,
        ]
    )
    process.communicate()


if __name__ == "__main__":
    mp4concat()

