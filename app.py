from flask import Flask, request, render_template
from google.cloud import storage

app = Flask(__name__)

# Configure your bucket name here
GCS_BUCKET = "flasktestbucket1"

def upload_to_gcs(file, bucket_name, destination_blob_name):
    """Uploads a file to the bucket."""
    # Create a client
    storage_client = storage.Client()  # This can stay, it handles public access too
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(destination_blob_name)

    # Upload the file
    blob.upload_from_file(file)

    # Make the file publicly accessible (optional)
    #blob.make_public()

    # Return the public URL
    public_url = f"https://storage.googleapis.com/{bucket_name}/{destination_blob_name}"
    return public_url

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'No file part'

    file = request.files['file']

    if file.filename == '':
        return 'No selected file'

    if file:
        # Upload the file to Google Cloud Storage
        public_url = upload_to_gcs(file, GCS_BUCKET, file.filename)

        return f'File successfully uploaded to {public_url}'

    return 'File upload failed'

if __name__ == '__main__':
    app.run(debug=True)

