def get_gcs_url(gcs_bucket_name:str, gcs_file_path:str) -> str:
    """Return Google Cloud Storage (URL) for given file path in a specific bucket.

    Args:
        gcs_bucket_name: A `String`. The name of GCS Bucket which the file exists in.
        gcs_file_path: A `String`. The complete path of requested file (must include extension).
    """
    return 'gs://'+gcs_bucket_name+'/'+gcs_file_path