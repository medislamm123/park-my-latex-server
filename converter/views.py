from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.core.files.storage import FileSystemStorage
from django.http import FileResponse, Http404
from django.conf import settings
from django.shortcuts import render


import subprocess
from pathlib import Path


@csrf_exempt  # Disable CSRF for this view, consider security implications
def convert_file(request):
    if request.method == "POST":
        # Example of handling file upload and conversion
        myfile = request.FILES["myfile"]
        fs = FileSystemStorage()
        file_name = myfile.name
        upload_file_path_relative = "input/" + file_name
        randomized_upload_file_path_relative = fs.save(upload_file_path_relative, myfile)
        uploaded_file_path = settings.MEDIA_ROOT / randomized_upload_file_path_relative
        output_file_path_relative = Path(randomized_upload_file_path_relative).parent.parent / ("output/" + Path(randomized_upload_file_path_relative).name.replace(
            ".tex", "_converted.tex"))
        output_file_path = settings.MEDIA_ROOT / output_file_path_relative
        modification_degree = request.POST.get("modificationdegree")

        command = [
            "parkmylatex",
            str(uploaded_file_path),
            str(output_file_path),
            "--degree",
            modification_degree,
        ]

        # Print the command list or convert it to a string for clearer visualization
        print("Executing command:", " ".join(command))

        subprocess.run(command,
            check=True,
        )

        download_url = (
            request.build_absolute_uri(reverse("download_view"))
            + "?file="
            + str(output_file_path_relative)
        )

        # Return a response, such as a direct download or a URL to the file
        return JsonResponse(
            {
                "message": "File converted successfully",
                "download_url": download_url,
            }
        )
    else:
        return JsonResponse(
            {"error": "This method only supports POST requests."}, status=405
        )


def download_view(request):
    # Get the relative file path from query parameters
    relative_file_path = request.GET.get("file")

    if not relative_file_path:
        raise Http404("No file specified.")

    # Construct the full path using MEDIA_ROOT safely with pathlib
    full_file_path = Path(settings.MEDIA_ROOT) / Path(relative_file_path)

    # Security check: Ensure the file is within MEDIA_ROOT to prevent directory traversal
    if (
        not full_file_path.is_file()
        or full_file_path.resolve().parent.parent != Path(settings.MEDIA_ROOT).resolve()
    ):
        raise Http404("Invalid file path.")

    # Serve the file
    return FileResponse(
        open(full_file_path, "rb"), as_attachment=True, filename=full_file_path.name
    )


def upload_page(request):
    return render(request, 'converter/upload_page.html')