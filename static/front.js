function handleChange(checkbox) {
    if(checkbox.checked == true){
        document.getElementById("url").removeAttribute("disabled");
        document.getElementById("loadart").setAttribute("disabled","disabled");

    }else{
        document.getElementById("url").setAttribute("disabled", "disabled");
        document.getElementById("loadart").removeAttribute("disabled");
   }
}
function loadart(){
	var selectorvalue = document.getElementById("selector").value;
	if(selectorvalue == "ntv"){
		$.getJSON("/n-tv",function(data){

			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
}
function checknearme(item){
	url = item.parentNode.getElementsByTagName("a")[0].href;
	console.log(url)
	
}
function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }
function createvid(item){
	item.setAttribute("disabled", "disabled");
	checkeds = document.getElementsByClassName("checked")
	counter = 0
	all_ = checkeds.length;
	console.log(all_)
	for (var i = checkeds.length - 1; i >= 0; i--) {
		
		var title = checkeds[i].getElementsByTagName("a")[0].innerHTML
		var $elem = checkeds[i].getElementsByTagName("a")[0];
		var URL = $("a", checkeds[i]).first().attr("alt");
		console.log({title:title,url:URL})
		counter += 1;
		document.getElementById("videogen").innerHTML = "<li class='list-group-item'><a id='"+URL.replace("https://www.n-tv.de/","").replace("/","")+"' target='_blank' href='"+URL+"' style='color:black;text-decoration:none'>"+title+"</a></li>"+document.getElementById("videogen").innerHTML;
		$.post("/video_gen_ntv",{url:URL})
			.done(function(data1){
						console.log(data1)
						
						if(data1.done == true){
							//done
							document.getElementById("perc").innerHTML = (100*counter)/all_+"%";
							
						}
						else{
							console.log("error")
						}
				})
	};
	document.getElementById("arts").style.display="none";
	document.scrollingElement.scrollIntoView();
	document.getElementById("videogen").style.display = "";

}