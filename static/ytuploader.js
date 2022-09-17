function checkTitle(filename){
    $.getJSON("/api/v1/get_video_title?q="+filename,function(data){
        document.getElementById("title").value = data.out;
    })
}