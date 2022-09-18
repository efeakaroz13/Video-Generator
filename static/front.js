function handleChange(checkbox) {
    if(checkbox.checked == true){
        document.getElementById("url").removeAttribute("disabled");
        document.getElementById("arts").style.display = "none";
        document.getElementById("videocreate").style.display = "";
        document.getElementById("loadart").setAttribute("disabled","disabled");

    }else{
    	document.getElementById("videocreate").style.display = "none";
        document.getElementById("url").setAttribute("disabled", "disabled");
        document.getElementById("arts").style.display = "";
        document.getElementById("loadart").removeAttribute("disabled");
   }
}
function loadart(){
	var selectorvalue = document.getElementById("selector").value;
	if(selectorvalue == "ntv"){
		$.getJSON("/n-tv",function(data){
			document.getElementById("arts").innerHTML = ""
			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	//storiestogrowby.org

	if(selectorvalue == "storiestogrowby.org"){
		$.getJSON("/list/storiestogrowby",function(data){
			document.getElementById("arts").innerHTML = ""
			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	if(selectorvalue == "fool.com"){
		$.getJSON("/list/fool",function(data){
			document.getElementById("arts").innerHTML = ""
			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	if(selectorvalue == "yahoo"){
		$.getJSON("/list/yahooNews",function(data){
			document.getElementById("arts").innerHTML = ""
			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	if(selectorvalue == "simplywall.st"){
		$.getJSON("/list/simplywall",function(data){
			document.getElementById("arts").innerHTML = ""
			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}

	if (selectorvalue == "my-personaltrainer.it") {

		$.getJSON("/personaltrainer_scraper_list",function(data){
			document.getElementById("arts").innerHTML = ""

			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})

	};
	if(selectorvalue == "healthy.thewom.it"){

		$.getJSON("/thwwomscrappe",function(data){
			document.getElementById("arts").innerHTML = ""

			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	if(selectorvalue == "netdoktor.de"){
		$.getJSON("/list/netdoktor",function(data){
			document.getElementById("arts").innerHTML = ""

			for (var i = data.out.length - 1; i >= 0; i--) {
				data.out[i]
				document.getElementById("arts").innerHTML = document.getElementById("arts").innerHTML+"<li><button type='button' onclick='checknearme(this)' style='margin-right:10px'></button><a  href='"+data.out[i]["href"]+"' alt='"+data.out[i]["href"]+"'>"+data.out[i]["title"]+"</a></li>"
			};
			document.getElementById("videocreate").style.display ="";
		})
	}
	console.log(selectorvalue)
}
function checknearme(item){
	url = item.parentNode.getElementsByTagName("a")[0].href;
	console.log(url)
	document.getElementById("url").value = url;

	
}
function sleep(ms) {
      return new Promise(resolve => setTimeout(resolve, ms));
   }
function createvid(item){
	item.setAttribute("disabled", "disabled");
	url = document.getElementById("url").value;
	choice = document.getElementById("selector").value;
	console.log(url);
	console.log(choice);
	if(choice == "my-personaltrainer.it"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/personal_trainer_video_gen_full?q="+url,function(data){

			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
		})
	}
	if(choice =="ntv"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/ntv_video_gen_full?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}
	if(choice =="fool.com"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/video/gen/fool?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}
	if(choice =="yahoo"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/video/gen/yahoo?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}

	if(choice =="netdoktor.de"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/video/gen/netdoktor?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}

	if(choice == "healthy.thewom.it"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/generate/thewom.it?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}
	if(choice == "storiestogrowby.org"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/video/gen/storiestogrowby?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}
	if(choice == "simplywall.st"){
		document.getElementById("fav").href = "/static/fav.gif";
		$.getJSON("/video/gen/simplywall?q="+url,function(data){
			console.log(data)
			document.getElementById("videocreate").style.display = "";
			item.removeAttribute("disabled");
			document.getElementById("fav").href = "/static/nofav.gif";
		})
	}
}