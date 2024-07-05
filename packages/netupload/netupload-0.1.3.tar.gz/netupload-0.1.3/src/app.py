import os
import argparse
from flask import Flask, request, render_template_string

app = Flask(__name__)

template_string = """
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <style>
      body {
        font-family: Arial, sans-serif;
        margin: 0;
        padding: 0;
        display: flex;
        justify-content: center;
        align-items: center;
        height: 100vh;
        background-color: #f0f0f0;
      }
      .container {
        background-color: white;
        padding: 50px;
        border-radius: 8px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
      }
      .file-input {
        margin-bottom: 20px;
      }
      .upload-button {
        background-color: #4caf50;
        color: white;
        border: none;
        padding: 10px 20px;
        cursor: pointer;
        border-radius: 5px;
      }
      .upload-button:hover {
        background-color: #45a049;
      }
    </style>
    <title>netupload</title>
    <!--<script>alert('Files uploaded successfully!');</script>-->
  </head>
  <body>
    <div class="container">
      <h2>netupload</h2>
      <form method="POST" enctype="multipart/form-data">
        <input type="file" name="file" class="file-input" multiple required />
        <br />
        <button type="submit" class="upload-button">Upload</button>
      </form>
    </div>
  </body>
</html>
"""


def save_files(files, save_directory):

    # Create the save directory if it does not exist
    if not os.path.exists(save_directory):
        os.makedirs(save_directory)

    # Save each file to the specified directory
    for file in files:
        file.save(os.path.join(save_directory, file.filename))


@app.route("/", methods=["GET", "POST"])
def upload_files():
    if request.method == "POST":
        files = request.files.getlist("file")
        save_files(files, app.config["SAVE_DIRECTORY"])
        return render_template_string(
            # Unlocks the success message, but otherwise sends the user
            # to the same starting page, feels like it is just reset.
            template_string.replace(
                "<!--<script>alert('Files uploaded successfully!');</script>-->",
                "<script>alert('Files uploaded successfully!');</script>",
            )
        )

    return render_template_string(template_string)


def run_server():
    parser = argparse.ArgumentParser(description="File Upload Server")
    parser.add_argument(
        "--save-dir",
        type=str,
        default="./uploads",
        help="Directory to save uploaded files",
    )
    parser.add_argument(
        "--host", type=str, default="0.0.0.0", help="Host to run the Flask server"
    )
    parser.add_argument(
        "--port", type=int, default=4000, help="Port to run the Flask server"
    )

    args = parser.parse_args()

    if not os.path.exists(args.save_dir):
        os.makedirs(args.save_dir)

    app.config["SAVE_DIRECTORY"] = args.save_dir

    app.run(host=args.host, port=args.port)


if __name__ == "__main__":
    run_server()
