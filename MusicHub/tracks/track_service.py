def get_filename_from_track(request):
    request.data["filename"] = request.data.get("track").name
    return request.data
