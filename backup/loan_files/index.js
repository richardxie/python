// 焦点图33g4
(function(d,D,v){d.fn.responsiveSlides=function(h){var b=d.extend({auto:!0,speed:1E3,timeout:7E3,pager:!1,nav:!1,random:!1,pause:!1,pauseControls:!1,prevText:"Previous",nextText:"Next",maxwidth:"",controls:"",namespace:"rslides",before:function(){},after:function(){}},h);return this.each(function(){v++;var e=d(this),n,p,i,k,l,m=0,f=e.children(),w=f.size(),q=parseFloat(b.speed),x=parseFloat(b.timeout),r=parseFloat(b.maxwidth),c=b.namespace,g=c+v,y=c+"_nav "+g+"_nav",s=c+"_here",j=g+"_on",z=g+"_s",
o=d("<ul class='"+c+"_tabs "+g+"_tabs' />"),A={"float":"left",position:"relative"},E={"float":"none",position:"absolute"},t=function(a){b.before();f.stop().fadeOut(q,function(){d(this).removeClass(j).css(E)}).eq(a).fadeIn(q,function(){d(this).addClass(j).css(A);b.after();m=a})};b.random&&(f.sort(function(){return Math.round(Math.random())-0.5}),e.empty().append(f));f.each(function(a){this.id=z+a});e.addClass(c+" "+g);h&&h.maxwidth&&e.css("max-width",r);f.hide().eq(0).addClass(j).css(A).show();if(1<
f.size()){if(x<q+100)return;if(b.pager){var u=[];f.each(function(a){a=a+1;u=u+("<li><a href='#' class='"+z+a+"'>"+a+"</a></li>")});o.append(u);l=o.find("a");h.controls?d(b.controls).append(o):e.after(o);n=function(a){l.closest("li").removeClass(s).eq(a).addClass(s)}}b.auto&&(p=function(){k=setInterval(function(){var a=m+1<w?m+1:0;b.pager&&n(a);t(a)},x)},p());i=function(){if(b.auto){clearInterval(k);p()}};b.pause&&e.hover(function(){clearInterval(k)},function(){i()});b.pager&&(l.bind("click",function(a){a.preventDefault();
b.pauseControls||i();a=l.index(this);if(!(m===a||d("."+j+":animated").length)){n(a);t(a)}}).eq(0).closest("li").addClass(s),b.pauseControls&&l.hover(function(){clearInterval(k)},function(){i()}));if(b.nav){c="<a href='#' class='"+y+" prev'>"+b.prevText+"</a><a href='#' class='"+y+" next'>"+b.nextText+"</a>";h.controls?d(b.controls).append(c):e.after(c);var c=d("."+g+"_nav"),B=d("."+g+"_nav.prev");c.bind("click",function(a){a.preventDefault();if(!d("."+j+":animated").length){var c=f.index(d("."+j)),
a=c-1,c=c+1<w?m+1:0;t(d(this)[0]===B[0]?a:c);b.pager&&n(d(this)[0]===B[0]?a:c);b.pauseControls||i()}});b.pauseControls&&c.hover(function(){clearInterval(k)},function(){i()})}}if("undefined"===typeof document.body.style.maxWidth&&h.maxwidth){var C=function(){e.css("width","100%");e.width()>r&&e.css("width",r)};C();d(D).bind("resize",function(){C()})}})}})(jQuery,this,0); 

$(function() {	
	//友情链接
	$("#linkShow").click(function(){
		$(this).hide();
		$("#linkHide").show();
		$("#linkStatus").removeClass("footlink");
	});
	$("#linkHide").click(function(){
		$(this).hide();
		$("#linkShow").show();
		$("#linkStatus").addClass("footlink");
	});
	if($(".f426x240").length){
			  $(".f426x240").responsiveSlides({
        auto: true,
        pager: true,
        nav: true,
        speed: 700,
        maxwidth: 2000
    });
		}

 
	$('.dropdownlist').hover(function(){	 		
	 		$("div",this).slideDown(150);
			$("span",this).css({background:'white'}); 
			$(".current b",this).css({"background-position":"-35px 0"});
	 	},function(){
			$("div",this).slideUp(25);
			 $("span",this).css({background:'transparent'}); 
			 $(".current b",this).css({"background-position":"1px 0"});
	 	});
 
    $(window).keydown(function(e) {
        if (e.which == 13 && $("#logindig").length == 0) {
			if($("#login_div").hasClass('none')){
				 $("#loginc").trigger("click");
				}else{
					$("input[type=button]",$("#login_div")).trigger("click");
				}
           
        }
    });
    if (BROWSER.ie == 6.0) {
        $("#iebox").show();
        $("#but_closeie,#but_closeie2").click(function() {
            $('#iebox').hide();
        });
    }
     
    $("input[name=keyword],input[name=pwd],input[name=sendnumber]").val('');

    $('input[name=keyword]').focus(function() {
        $("label[for=keyword],label[for=kwd]").text('');
    }).blur(function() {
        if (($(this).val()).length < 1) {
            $("label[for=keyword],label[for=kwd]").text('用户名/手机号');
        }
    });
    $('input[name=pwd]').focus(function() {
        $("label[for=pwd]").text('');
    }).blur(function() {
        if (($(this).val()).length < 1) {
            $("label[for=pwd]").text('登录密码');
        }
    });
    $('input[name=sendnumber]').focus(function() {
		$(".validate").prop("src","/Index/verify/"+Math.random());
        $("label[for=sendnumber]").text('');
    }).blur(function() {
        if (($(this).val()).length < 1) {
            $("label[for=sendnumber]").text('验证码');
        }
    });
  
 
 
	checkCookie();
	if ($.browser.msie && $.browser.version == "6.0") {
		$.idialog.show({
			icon: "normal",
			title: "系统提示",
			msg: "	您使用的是IE6浏览器，强烈建议您使用IE8及更高版本的浏览器！",
			showMask: false
		});
	}
	 
        
         

});


function index_login(){
 
	 
		var keywords = $("#keyword").val();
		var cookietime = $("#cookietime").val();
		var sendnumbers = $("#sendnumber").val();
		if (!keywords ||  !$("#password").val()) {
		 $.idialog.show({
							icon: "normal",
							title: "系统提示",
							msg: "请填写用户名，密码，验证码"
						});
			return false;
		}

		var pwds = encrypt("password", sendnumbers);
		 //var pwds =  $("#password").val();

		$.ajax({
			type: 'POST',
			dataType: "json",
			url: '/Index/checklogin',
			data: {
				username: keywords,
				password: pwds,
				cookietimes: cookietime
			//	sendnumbers:sendnumbers
			},
			beforeSend: function(){
				$(".loginc").val("登陆中....");
				}, 
			success: function(data) {
				if (data.status == "1") {
					$("Body").append('<div display="none">' + data.msg + '</div>');
					window.setTimeout(function() {
						window.location.href =data.location
					}, 300);
				} else if(data.status =='3'){
					$(".loginc").val("登陆");
					if (data.status == "10") {
						$.idialog.show({
							icon: "normal",
							title: "系统提示",
							msg: "我们正在努力上线中，请不要操作！如有疑问，请拨打0755-21624348。"
						});
					}else{
						$.idialog.show({
							icon: "normal",
							title: "系统提示",
							msg: "用户名或密码有误"
						});
						}
					 
				}else if(data.status==4){
					     $.idialog.show({
							icon: "normal",
							title: "系统提示",
							msg:data.msg
						});
					}else if(data.status =='12'){
                                    $.idialog.show({
							icon: "normal",
							title: "系统提示",
							msg: "错误次数超过10次，请2小时后再登录"
						});
            }else if (data.status ==2){//有体验金、登录到体验版
                $("Body").append('<div display="none">' + data.msg + '</div>');
                window.setTimeout(function(){ window.location.href = 'http://tiyan.itbt.com.cn/Account'},300);
            }
        }
    })


}

function checkCookie(){
    var cookieEnabled=(navigator.cookieEnabled)? true : false   
    if (typeof navigator.cookieEnabled=="undefined" && !cookieEnabled){ 
        document.cookie="testcookie";
        cookieEnabled=(document.cookie.indexOf("testcookie")!=-1)? true : false;
    }
    return (cookieEnabled)?true:showCookieFail();
}

function showCookieFail(){
 	$.idialog.show({
			icon: "normal",
			title: "系统提示",
			msg: " o(︶︿︶)o ，您的浏览器已经禁用了cookie,将无法正常使用本站的服务,<br><p>解决办法--->:<a style='color:red' href='http://jr.yatang.cn/Public/help/acateid/149'>阅读</a></p>",
			showMask: false
		});
}