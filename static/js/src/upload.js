function redirect() {
    location.href = "/articles";
}

function upload() {
    var formData = new FormData($("upload_form")[0]);
    $.ajax({
        url: "/api/file/upload",
        type: "POST",
        data: formData,
        async: false,
        cache: false,
        contentType: false,
        processData: false,
        success: function(data) {
            if (data["msg"] == "success") {
                redirect();
            } else {
                alert("上传失败");
            }
        },
        error: function(data) {
            alert("上传失败");
        }
    });
}

$(document).ready(function() {
    $("#submit").click(upload);
});
