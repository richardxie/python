var disallowfloat = 'newthread';
var SITEURL = 'http://jr.yatang.cn/';
var IMGDIR = 'Public/Images/';
var BROWSER = {};
//Navigator 对象包含有关浏览器的信息
var USERAGENT = navigator.userAgent.toLowerCase();
browserVersion({'ie':'msie','firefox':'','chrome':'','opera':'','safari':'','mozilla':'','webkit':'','maxthon':'','qq':'qqbrowser'});
if(BROWSER.safari) {
	BROWSER.firefox = true;
}
BROWSER.opera = BROWSER.opera ? opera.version() : 0;

HTMLNODE = document.getElementsByTagName('head')[0].parentNode;
if(BROWSER.ie) {
	BROWSER.iemode = parseInt(typeof document.documentMode != 'undefined' ? document.documentMode : BROWSER.ie);
	HTMLNODE.className = 'ie_all ie' + BROWSER.iemode;
}
 

if(BROWSER.firefox && window.HTMLElement) {
	HTMLElement.prototype.__defineGetter__( "innerText", function(){
		var anyString = "";
		var childS = this.childNodes;
		for(var i=0; i <childS.length; i++) {
			if(childS[i].nodeType==1) {
				anyString += childS[i].tagName=="BR" ? '\n' : childS[i].innerText;
			} else if(childS[i].nodeType==3) {
				anyString += childS[i].nodeValue;
			}
		}
		return anyString;
	});
	HTMLElement.prototype.__defineSetter__( "innerText", function(sText){
		this.textContent=sText;
	});
	HTMLElement.prototype.__defineSetter__('outerHTML', function(sHTML) {
			var r = this.ownerDocument.createRange();
		r.setStartBefore(this);
		var df = r.createContextualFragment(sHTML);
		this.parentNode.replaceChild(df,this);
		return sHTML;
	});

	HTMLElement.prototype.__defineGetter__('outerHTML', function() {
		var attr;
		var attrs = this.attributes;
		var str = '<' + this.tagName.toLowerCase();
		for(var i = 0;i < attrs.length;i++){
			attr = attrs[i];
			if(attr.specified)
			str += ' ' + attr.name + '="' + attr.value + '"';
		}
		if(!this.canHaveChildren) {
			return str + '>';
		}
		return str + '>' + this.innerHTML + '</' + this.tagName.toLowerCase() + '>';
		});

	HTMLElement.prototype.__defineGetter__('canHaveChildren', function() {
		switch(this.tagName.toLowerCase()) {
			case 'area':case 'base':case 'basefont':case 'col':case 'frame':case 'hr':case 'img':case 'br':case 'input':case 'isindex':case 'link':case 'meta':case 'param':
			return false;
			}
		return true;
	});
}

(function ($)
{
    var ajaxErr = true;
	 //全局系统对象
    window['UI'] = {};
    
    UI.Loadjs=function (jsFileURL){
		var head = document.getElementsByTagName('HEAD').item(0); 
		 var script = document.createElement('SCRIPT'); 
		 script.src = jsFile; 
		 script.type = "text/javascript"; 
		 head.appendChild(script); 
	};
	UI.Post=function(url,params,okfunc){
          /*      setTimeout(function(){
                    if(ajaxErr){
                        alert("ajax系统异常,请稍后再试"); 
                    }
                },10000);*/ //单位毫秒 
		$.ajax({
			dataType:'json',
			type: 'POST',  
	        url:url,
	        data:params,	
			timeout:  20000,
	        success: function(data){
                       //     ajaxErr = false;
			    if(typeof(okfunc)=="function"){
			    	okfunc(data);
			    }
		    },
			error:function(){
					$.idialog.show({
			icon: "normal",
			title: "系统提示",
			msg: "Sorry!数据加载失败！请稍后再试",
			showMask: false
		});
				
				} 
			
					});
	};
	UI.Page=function (arg){
 var starpage=arg.star;

		var pageNumber=arg.star;
		 starpage=pageNumber?pageNumber:1;
		var pagesize=arg.size;	
		var total=arg.total;
		var toObj=arg.toObj; 
		var maxpage=Math.ceil(total/pagesize);  
		var viewmaxpage=maxpage;
		var ChangepageEvent=arg.changepage; 
 
/* var starpage=arg.star;
		var pageNumber=arg.star;
		if(pageNumber<9){
			starpage=1;
		}else if(pageNumber==9){
			starpage=3;
		}else{
			ypart=(pageNumber+2)%10;
			zpart=parseInt(pageNumber/10);
			starpage=zpart%10+ypart;			
		}
		var pagesize=arg.size;	
		var total=arg.total;
		var toObj=arg.toObj;
		var maxpage=Math.ceil(total/pagesize);
	 
		var viewmaxpage=maxpage;
		var ChangepageEvent=arg.changepage;
		*/
		
		function Biuldpageview(){ 
		
			//最大页码
/*			maxpage=Math.ceil(total/pagesize);
		 	  
			  viewmaxpage=maxpage;
			 if((maxpage-starpage)>9)
			 {			 viewmaxpage=starpage+9;			 }		
			//最大页码  */
				maxpage=Math.ceil(total/pagesize);
				if(maxpage==0){
					return false;
					}
	 		var offset=2;
				var num=5;//显示7个页码
				if(maxpage<num){
					num=maxpage;
					}
			  viewmaxpage=maxpage ;
			  starpage=starpage<0?1:starpage;  
				viewmaxpage=starpage+offset;
				viewmaxpage=viewmaxpage>maxpage?maxpage:viewmaxpage;
				
				if(starpage+offset<=maxpage){
					starpage-=offset
					}else{
						starpage=maxpage-num+1;
					  
						} 
			 
					if(starpage<=1){
						starpage=1;
						
						viewmaxpage=num;
						}
					if(starpage==maxpage ){
						starpage=maxpage-num;
						starpage=starpage<1?1:starpage;
						viewmaxpage=maxpage;
						}  
						
			 //页码显示范围   starpage---viewmaxpage
			 var Htmlstr='<ul><li class="page02">';
			// Htmlstr+='共 ' + maxpage + ' 页</li>';			 
			 Htmlstr+="<li class='page07'> <span tag='p' >上一页</span></li>";
			 Htmlstr+="<li class='page01'>" ;	
			 	 if( pageNumber>4){
					 	 Htmlstr+="<span tag=1>1</span>";
				 Htmlstr+="<span class='noclick' onclick='return false;'>...</span>";
			
				 }		 
			 for (var i=starpage;i<=viewmaxpage;i++)
			 {
				 if(i==pageNumber){
					 Htmlstr+="<span id='page05' tag="+i+">"+i+"</span>";
				 }else{
					 Htmlstr+="<span tag="+i+">"+i+"</span>";
				 } 
			 }	 
	 
			 if( pageNumber<maxpage-1&&viewmaxpage<maxpage){
				 Htmlstr+="<span class='noclick'>...</span>";
				 Htmlstr+="<span tag="+maxpage+">"+maxpage+"</span>";
				 }
				 
			 Htmlstr+="</li>";
			 Htmlstr+="<li class='page07'> <span tag='n' >下一页</span></li>";	
			 Htmlstr+="<li class='page02'>";		 
			 Htmlstr+="<p class='f-l'>跳到</p><input type='text' id='JpageNumb' class='page03' /><p class='f-l'>页</p>";
			 Htmlstr+="<input class='page04 f-l'  type='button'  tag='j'  value='确定' />";		 
			 Htmlstr+="</li>";		
			 if(maxpage>1){
				 	 toObj.html(Htmlstr);	
				 }	 
			
			 toObj.find("span").bind('click',click); 
			 toObj.find(".page04").bind('click',click);
			 toObj.find(".noclick").unbind('click',click); 
		}
		function SelectPage(ppage,ptotal){
				 starpage=ppage;  
				var maxpage=Math.ceil(ptotal/pagesize);
			 
				Biuldpageview();
		 };
		 this.currpage=function (p){
			 pageNumber=p;
		 }
		 this.settotal=function(ptotal,selectpage){
			 var bereview=false;
			if(total!=ptotal){
				total= ptotal;
				 maxpage=Math.floor(total/pagesize);
					if((total%pagesize)>0){
						maxpage+=1;
					}
				// toObj.find(".page02")[0].innerHTML ='共 ' + maxpage + ' 页';//.bind('click',click);
			}
			 
			 if(selectpage>0 && selectpage!=pageNumber){
				  toObj.find('#page05').attr("id", '');
				  pageNumber=selectpage;
				  if(maxpage>viewmaxpage && pageNumber>(starpage+8)){
					   //这里访问 类方法
					  bereview=true; 
					  SelectPage(pageNumber,total);
				   }else if(starpage>1 && pageNumber<(starpage+1)){
					   bereview=true;
					   
					   SelectPage(pageNumber,total);
				   }else{
					   toObj.find("[tag='"+ pageNumber +"']").attr('id','page05');
				   }	
			 }
 
			 if(bereview==false && (viewmaxpage==0 || (viewmaxpage-starpage)>maxpage||((viewmaxpage-starpage)<9 && maxpage>=(viewmaxpage-starpage)) )){
				// if(maxpage>(viewmaxpage-starpage)){
				// console.log('total_2:'+total+",starpage_2:"+starpage+",viewmaxpage_2:"+maxpage+",bereview_2:"+bereview); 
					 SelectPage(pageNumber,total);
				// }
			 }
		 };
		this.init=function(){
			Biuldpageview()	;		 
		};
		
		this.selectPage=function(ppage,ptotal){ 
			SelectPage(ppage,ptotal);
		};
		function click(Page,e){
			var old=pageNumber;
			var Key=Page.target.getAttribute('tag');	
			 switch (Key) {
			 	case 'f':
			 		pageNumber=1;
			    break;
			 	case 'p':
			 		pageNumber-=1;
			    break;
			 	case 'n':
			 		pageNumber+=1;
			    break;
			 	case 'l':
			 		pageNumber=maxpage;
				    break;
			 	case 'j':
			 	    var inp=toObj.find("#JpageNumb").val();
			 	   if(inp!=undefined&&inp!='')
			 	   {
			 	     pageNumber=parseInt(inp);
			 	 	 if(pageNumber<1){pageNumber=1;} 
			 		 if(pageNumber>maxpage){pageNumber=maxpage;}	
			 	    }
				    break;
			 	 default:
			 		pageNumber=parseInt(Key);
			 	    
			 }
			 if(pageNumber<1){
				 pageNumber=1;
			 }else if(pageNumber>maxpage){
				 pageNumber=maxpage;
			 }
			 if(old!=pageNumber){
				 if(ChangepageEvent){
					 ChangepageEvent(this,pageNumber,pagesize);
				 }
			 }
		   toObj.find('#page05').attr("id", '');		  
		   if(maxpage>viewmaxpage && pageNumber>(starpage+8)){
			   //这里访问 类方法
			  SelectPage(pageNumber,total);
		   }else if(starpage>1 && pageNumber<(starpage+1)){
			   SelectPage(pageNumber,total);
		   }else{
			   toObj.find("[tag='"+ pageNumber +"']").attr('id','page05');
		   }					 
	    }; 
	 
		this.GetParams=function(){
			return {'page':pageNumber,'size':pagesize};
		};
		Biuldpageview(); 
	}; 
    UI.loadPage=function(id, url){ 	    
    	if(url.indexOf("loginup")==-1){   //弹出的登陆框去掉转圈，网速慢的时候一直加载
			$("#"+id).addClass("loader"); 
			$("#"+id).append('<img src="' + IMGDIR + '/loading.gif"> 请稍候...'); 
    	}
		$.ajax({ 
			type: "get", 
			url: url, 
			cache: false, 
			error: function() {alert('加载页面' + url + '时出错！');}, 
			success: function(msg) { 
				//document.getElementById(id).innerHTML  = msg;
				$("#"+id).html(msg); 
				$("#"+id).removeClass("loader"); 
			} 
		}); 
	};
	 UI.loading=function(msg,pobjname){
		 var sd_width =  400; 
		 if(isNull(pobjname)){
			 pobjname="body";
			 $("body","html").css({height: "100%", width: "100%"});
		 }
		 if(document.getElementById("SD_overlay1") === null) {
				
				
				if( pobjname!="body"){
					$(pobjname).append("<div id='SD_overlay1'></div>");
					$("#SD_overlay1").addClass("SD_overlayBG3");
					$("#SD_overlay1").width( $(pobjname).width());
					$("#SD_overlay1").height( $(pobjname).height());
				}else{
					$(pobjname).append("<div id='SD_overlay'></div>");
					$("#SD_overlay").addClass("SD_overlayBG3");
				}
				 
		 }
		 $(pobjname).append("<div id='SD_window'></div>");
		 var SD_html=Biulddialoghtml(msg,'writing');			 
		 $("#SD_window").append(SD_html);
		 $("#SD_body").width(sd_width - 50);
		 sd_load(sd_width);
		 $("#SD_window").show();	
	 };
	 UI.showinfo=function(msg,pimg){
		 var sd_width =  400; 
		 //info  warn help writing
		 
		 $("body").append("<div id='SD_window'></div>");
		 var SD_html=Biulddialoghtml(msg,pimg);			 
		 $("#SD_window").append(SD_html);
		 $("#SD_body").width(sd_width - 50);
		 sd_load(sd_width);
		 $("#SD_window").show();
		 setTimeout(function(){sd_remove();},1000);
	 };
	 function Biulddialoghtml(msg,pimg){
		 var imgs = pimg ? pimg : 'info';
		 var SD_html;
			SD_html = "";
			SD_html += "<div id='SD_container'>"; 
			SD_html += "<div id='SD_body'>";
			//SD_html += "<b class='"+ imgs +"'><b>";
			SD_html +="<div id='SD_content' class='"+ imgs +"'>" + msg + "</div></div>";
			SD_html += "</div>";
			SD_html += "</div>";
		return 	SD_html;
	 }
	 
	 UI.RemoveInfodiv=function(){
		 sd_remove();
	 }
	 UI.showDialog=function(mode, msg, t, sd_width,sufunc,cancelfun) {
			var sd_width = sd_width ? sd_width : 400;
			var mode = in_array(mode, ['confirm', 'window', 'info', 'loading']) ? mode : 'alert';
			var t = t ? t : "提示信息";
			var msg = msg ? msg : "";
			var confirmtxt = confirmtxt ? confirmtxt : "确定";
			var canceltxt = canceltxt ? canceltxt : "取消";
			sd_remove();
			try {
				if(typeof document.body.style.maxHeight === "undefined") {
					$("body","html").css({height: "100%", width: "100%"});
					if(document.getElementById("SD_HideSelect") === null) {
						$("body").append("<iframe id='SD_HideSelect'></iframe><div id='SD_overlay'></div>");
					}
				} else {
					if(document.getElementById("SD_overlay") === null) {
						$("body").append("<div id='SD_overlay'></div>");
					}
				}
				if(mode == "alert") {
					if(detectMacXFF()) {
						$("#SD_overlay").addClass("SD_overlayMacFFBGHack");
					} else {
						$("#SD_overlay").addClass("SD_overlayBG");
					}
				} else {
					if(detectMacXFF()) {
						$("#SD_overlay").addClass("SD_overlayMacFFBGHack2");
					} else {
						$("#SD_overlay").addClass("SD_overlayBG2");
					}
				}
				$("body").append("<div id='SD_window'></div>");
				var SD_html;
				SD_html = "";
				SD_html += "<div id='SD_container'>";
				SD_html += "<div id='SD_body1'>";
				SD_html += "<h3 id='SD_title'>" + t + "</h3>";
				SD_html += "<div id='SD_body'><div id='SD_content'>" + msg + "</div></div>";
				SD_html += "<div id='SD_button'><div class='SD_button'>";
				SD_html += "<a id='SD_confirm'>" + confirmtxt + "</a>";
				SD_html += "<a id='SD_cancel'>" + canceltxt + "</a>";
				SD_html += "</div></div>";
				SD_html += "<a href='javascript:;' id='SD_close' title='关闭'></a>";
				SD_html += "</div>";
				SD_html += "</div>";
				$("#SD_window").append(SD_html);
				$("#SD_confirm").bind("click", function(){					 
					sd_remove();
				});
				$("#SD_confirm,#SD_cancel,#SD_close").bind("click", function(){
					sd_remove();
					
				});
				if(mode == "info" || mode == "alert") {
					$("#SD_cancel").hide();
					$("#SD_button").show();
				}
				if(mode == "window") {
					$("#SD_close").show();
				}
				if(mode == "confirm") {
					$("#SD_button").show();
				}
				var sd_move = false;
				var sd_x, sd_y;
				$("#SD_container > h3").click(function(){}).mousedown(function(e){
					sd_move = true;
					sd_x = e.pageX - parseInt($("#SD_window").css("left"));
					sd_y = e.pageY - parseInt($("#SD_window").css("top"));
				});
				$(document).mousemove(function(e){
					if(sd_move){
						var x = e.pageX - sd_x;
						var y = e.pageY - sd_y;
						$("#SD_window").css({left:x, top:y});
					}
				}).mouseup(function(){
					sd_move = false;
				});
				$("#SD_body").width(sd_width - 50);
				sd_load(sd_width);
				$("#SD_window").show();
				$("#SD_window").focus();
			} catch(e) {
				alert("System Error !");
			}
		};
		//+---------------------------------------------------
		//| 比较日期差 dtEnd 格式为日期型或者 有效日期格式字符串
		//+---------------------------------------------------
		UI.DateDiff = function(strInterval,dtStart, dtEnd) {
			var dtStart = dtStart;
			if (typeof dtEnd == 'string' )//如果是字符串转换为日期型
			{
			dtEnd = StringToDate(dtEnd);
			}
			switch (strInterval) {
			case 's' :return parseInt((dtEnd - dtStart) / 1000);
			case 'n' :return parseInt((dtEnd - dtStart) / 60000);
			case 'h' :return parseInt((dtEnd - dtStart) / 3600000);
			case 'd' :return parseInt((dtEnd - dtStart) / 86400000);
			case 'w' :return parseInt((dtEnd - dtStart) / (86400000 * 7));
			case 'm' :return (dtEnd.getMonth()+1)+((dtEnd.getFullYear()-dtStart.getFullYear())*12) - (dtStart.getMonth()+1);
			case 'y' :return dtEnd.getFullYear() - dtStart.getFullYear();
			}
		}
		UI.SetSingValue= function(cobj,pvalue) {
			SetSValue(cobj,pvalue);
		}
		function SetSValue(cobj,pvalue){		 
				if(cobj!=null) {
					var  format=cobj.attr('format');
					if(!UI.isempty(format)) {
						var type =1; //1 string 2 money 3 uintime to date
						if(format.indexOf('3')>=0){	
							if(isNull( pvalue)){
								cobj.html('无');
							}else{
								cobj.html(format.replace('3',UI.timeFormat(pvalue,'yyyy-MM-dd')));
							}							 
						}else if(format.indexOf('2')>=0){							
							 cobj.html(format.replace('2',UI.Money(pvalue)));
						}else if(format.indexOf('1')>=0){
							if(isNull( pvalue)){
								cobj.html('无');
							}else{
							   cobj.html(format.replace('1',pvalue));
							}
						}						
					 }else{
						 if(isNull( pvalue)){
								cobj.html('无');
							}else{
									cobj.html(pvalue);
							}
					 }	
				}
		}
		UI.SetValue=function(obj,pdata){
			for ( var key  in pdata) {
				 cobj=obj.find('#UI'+key);
				 SetSValue(cobj,pdata[key]);				 
			}
			return true;
		}
		//截取小数
		UI.Money=function (pMoney){
			if(isNull(pMoney) ){
				 return  "0.00";
			}
			pMoney=pMoney.toString()
			var tmp=pMoney.indexOf(".");
		     back="";
			if(tmp==-1){
				back=pMoney +'.00';
			}else{
				back=pMoney.substring(0,tmp + 3);
			}
		    return  back;
		}
		//时间处理
		UI.timeFormat = function(punixtime,fmt)   
		{ 
		  var unixTimestamp = new Date(punixtime* 1000); 
		  
		  var o = {   
		    "M+" : unixTimestamp.getMonth()+1,                 //月份   
		    "d+" : unixTimestamp.getDate(),                    //日   
		    "h+" : unixTimestamp.getHours(),                   //小时   
		    "m+" : unixTimestamp.getMinutes(),                 //分   
		    "s+" : unixTimestamp.getSeconds(),                 //秒   
		    "q+" : Math.floor((unixTimestamp.getMonth()+3)/3), //季度   
		    "S"  : unixTimestamp.getMilliseconds()             //毫秒   
		  };   
		  if(/(y+)/.test(fmt))   
		    fmt=fmt.replace(RegExp.$1, (unixTimestamp.getFullYear()+"").substr(4 - RegExp.$1.length));   
		  for(var k in o)   
		    if(new RegExp("("+ k +")").test(fmt))   
		  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
		  return fmt;   
		} ;
		function sd_load(sd_width) {
			if(sd_width) {
				$("#SD_window").css("width", sd_width + "px");
			}
			var sd_top = ($(window).height() - $("#SD_window").height()) / 2 + $(document).scrollTop();
			if(sd_top < 0) {
				sd_top = 0;
			}
			var sd_left = ($(window).width() - $("#SD_window").width()) / 2;
			if(sd_left < 0) {
				sd_left = 0;
			}
			$("#SD_window").css("top", sd_top);
			$("#SD_window").css("left", sd_left);
		}
		function detectMacXFF() {
			var userAgent = navigator.userAgent.toLowerCase();
			if(userAgent.indexOf("mac") != -1 && userAgent.indexOf("firefox") != -1) {
				return true;
			}
		}
		function sd_remove() {
			$("#SD_close,#SD_cancel,#SD_confirm").unbind("click");
			$("#SD_window,#SD_overlay,#SD_overlay1,#SD_HideSelect").remove();
			if(typeof document.body.style.maxHeight == "undefined") {
				$("body","html").css({height: "auto", width: "auto"});
			}
		}
		function in_array(needle, haystack) {
			if(typeof needle == "string" || typeof needle == "number") {
				for(var i in haystack) {
					if(haystack[i] == needle) {
						return true;
					}
				}
			}
			return false;
		}
	  UI.isempty=function(p){
		  return isNull(p);
	  }
	  function isNull(variable) {
			if(typeof variable == 'undefined'){
				return true;
			}else if(variable==""){
				return true;
			}else if(variable==null){
				return true;
			}
			return false;			 
		}
	 
})(jQuery);
 
function loginform(e){
		$("#append_parent").html('');
		$("#append_parent").load( '/Login/loginup');
//		
//	if( $("#logindig").length>0){
//		$("#logindig").show();
//	}else{
//		
//		UI.loadPage('append_parent', '/Login/loginup');
//	}	 
}



function browserVersion(types) {
	var other = 1;
	for(i in types) {
		var v = types[i] ? types[i] : i;
		if(USERAGENT.indexOf(v) != -1) {
			var re = new RegExp(v + '(\\/|\\s)([\\d\\.]+)', 'ig');
			var matches = re.exec(USERAGENT);
			var ver = matches != null ? matches[2] : 0;
			other = ver !== 0 && v != 'mozilla' ? 0 : other;
		}else {
			var ver = 0;
		}
		eval('BROWSER.' + i + '= ver');
	}
	BROWSER.other = other;
}

function setCookie(NameOfCookie, value, expiredays) {
	var ExpireDate = new Date();
	ExpireDate.setTime(ExpireDate.getTime() + (expiredays * 24 * 3600 * 1000));
	document.cookie = NameOfCookie + "=" + escape(value) + ((expiredays == null) ? "": "; expires=" + ExpireDate.toGMTString());
}

function getCookie(NameOfCookie) {
	if (document.cookie.length > 0) {
		begin = document.cookie.indexOf(NameOfCookie + "=");
		if (begin != -1) {
			begin += NameOfCookie.length + 1; //cookie值的初始位置   
			end = document.cookie.indexOf(";", begin); //结束位置   
			if (end == -1) end = document.cookie.length; //没有;则end为字符串结束位置  
			//document.write(document.cookie.substring(begin, end));
			return unescape(document.cookie.substring(begin, end));
		}
	}
	return null;
}

function delCookie(NameOfCookie) {
	if (getCookie(NameOfCookie)) {
		document.cookie = NameOfCookie + "=" + ";expires=Thu, 01-Jan-70 00:00:01 GMT";
	}
}

function showTime(tenderid, time_distance) {
  this.tenderid = tenderid;
  //PHP时间是秒，JS时间是微秒 
  this.time_distance = time_distance * 1000;
}
showTime.prototype.setTimeShow = function () {
  var timer = $('.lefttime_' + this.tenderid);
  var str_time;
  var int_day,
  int_hour,
  int_minute,
  int_second;
  time_distance = this.time_distance;
  this.time_distance = this.time_distance - 1000;
  if (time_distance > 0) {
    int_day = Math.floor(time_distance / 86400000);
    time_distance -= int_day * 86400000;
    int_hour = Math.floor(time_distance / 3600000);
    time_distance -= int_hour * 3600000;
    int_minute = Math.floor(time_distance / 60000);
    time_distance -= int_minute * 60000;
    int_second = Math.floor(time_distance / 1000);
    if (int_hour < 10)
    int_hour = '0' + int_hour;
    if (int_minute < 10)
    int_minute = '0' + int_minute;
    if (int_second < 10)
    int_second = '0' + int_second;
	 
	if(int_day){
		 str_time = int_day + '天';
		}else{
			str_time="";
			
			}		   
			 str_time +=  int_hour + '小时' + int_minute + '分钟' + int_second + '秒';
    timer.text(str_time);
    var self = this;
    setTimeout(function () {
      self.setTimeShow();
    }, 1000);
    //D:正确 
  } else {
    timer.text('已满标或过时');
    return ;
  }
}
//弹窗水平居中
function popcenterWindow(divID){
//    var windowHeight=$(window).height(); //获得窗口的高度 
    var windowWidth=$(window).width(); //获得窗口的宽度 
//    var popHeight=$(divID).height(); //获得弹窗的高度 
    var popWidht=$(divID).width();//获得弹窗的宽度 
//    var scrollTop=$(window).scrollTop(); //获得滚动条的高度 
//    var scrollleft=$(window).scrollLeft(); //获得滚动条的宽度 
//    var popY=(windowHeight-popHeight)/2; 
    var popX=(windowWidth-popWidht)/2;  
    $(divID).css({'left':popX,'z-index':4});
}
/**
*格式化金额
* @param amount INT 
*/
function moneyFormat(amount) {
    var delimiter = ","; // replace comma if desired
    amount = new String(amount);
    var a = amount.split('.',2);
	console.log(a);
    var d = a[1];
    var i = a[0];
    if(isNaN(i) || !(/^[1-9][0-9]{0,12}$/.test(i))) { return amount; }
    var minus = '';
    if(i < 0) { minus = '-'; }
    i = Math.abs(i);
    var n = new String(i);
    var a = [];
    while(n.length > 3)
    {
        var nn = n.substr(n.length-3);
        a.unshift(nn);
        n = n.substr(0,n.length-3);
    }
    if(n.length > 0) { a.unshift(n); }
    n = a.join(delimiter);
    if(!d || d.length < 1) { amount = n; }
    else { amount = n + '.' + d; }
    amount = minus + amount;
    return amount;
}