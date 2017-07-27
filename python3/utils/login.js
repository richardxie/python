(function(){
	
	function emptyErrorMsg(ele){
        $(ele).empty();
    }
	
    //显示验证码
    function errorAndshowCode(msg,showVcode){
    	//修复360浏览器捕捉到验证码显示事件进行错误提示
        if(msg != null && msg.indexOf('不显示验证码') < 0 ){
        	$('.js-warn').hide();
        	$('.js-error').show();
        	$('.js-error').html(msg);
        }
        if(true == showVcode){
        	$('#login_vocde').click();
        	$('.js-code').show();
        }
        $('.js-clear').show();
        $('.js-password').focus();
    }
    
    function getRequestParam(method){
    	var timestamp = new Date().Format("yyyy-MM-dd hh:mm:ss"); 
    	var origin = $("#origin").val();
    	origin = origin?origin:"1";
    	var appKey = "0000"+origin;
    	var source = $("#source").val();
    	var synUrl = $("#synUrl").val();
    	var data = {
    		format:'json',
    		appKey:appKey,
    		v:'1.0',
    		timestamp:timestamp,
    		method:method,
    		origin:origin,
    		source:source,
    		synUrl:synUrl
    	};
    	return data;
    }
    
    //用户名输入错误
    function errorShow(msg){
    	$('.js-warn').hide();
        $('.js-error').html(msg);
        $('.js-error').show();
        $('.js-clear').show();
        $('.js-password').focus();
    }
    
    //验证码
    function changeVcod(){
        // 用于点击时产生不同的验证码
        $(this).attr("src","vcode.jpg?time="+new Date().getTime());
    }

    //显示验证码
    function showVcode(){
    	var userName = $('#js-username').val();
    	if("" == userName || undefined == userName || null == userName){
    		return;
    	}
    	var data = getRequestParam('sso.showVcode');
    	data.u = userName;
    	$.ajax({
    		type : 'post',
    		url : './yluser',
    		data:data,
    		dataType : 'json',
    		async : true,
    		success : function(data) {
    			if(data.code == '0'){
    				$('#login_vocde').click();
    	        	$('.js-code').show();
		    	   return;
    		    }
    		},
    		error : function(e) {
               return;
    		}
    	});
    }
    
    //注册跳转
    function regUrl(){
    	var regUrl = $("#regUmp").attr('regUrl');
    	ytUtil.ytRedirect(regUrl);
    }
    
    //找回密码
    function findPwdUrl(){
    	var findPwdUrl = $("#findPwdUmp").attr('findPwdUrl');
    	ytUtil.ytRedirect(findPwdUrl);
    }
    
    //登录
    function loginFunction(){
    	var user = $('#js-username').val();
    	if(null == user || '' == user || user == undefined){
    		errorShow('用户名不容许为空!');
    		return;
    	}
    	var pwd = $('#js-password').val();
    	if(null == pwd || '' == pwd || pwd == undefined){
    		errorShow('密码不容许为空!');
    		return;
    	}
    	var data = getRequestParam('sso.login');
    	data.u = user;
    	data.p = ytUtil.encrypt(pwd,data.timestamp);
    	data.vcode = $('#js-code').val();
    	data.cookieAge = $('#_cache_time').val();
        $.ajax({
    		type : 'post',
    		url : './yluser',
    		data:data,
    		dataType : 'json',
    		async : true,
    		success : function(data) {
    			if(data.code == '0'){
		    	   if(data.isRedirect){
		    		    ytUtil.ytRedirect(data.redirectUrl);
		    	   		return;
		    	   }
		    	   //其他处理
		    	   return;
    		    }
    			errorAndshowCode(data.message,data.data);
    		},
    		error : function(e) {
                errorAndshowCode(e,true);
    		}
    	});
    }
    $('#js-password').on('blur', function(){
    	$('.css-log-error').hide();
    	$('.css-log-warn').show();
    });
    $('#js-login').on('click', loginFunction);
    $('#regUmp').on('click', regUrl);
    $('#findPwdUmp').on('click', findPwdUrl);
    $('#js-username').on('blur',showVcode);
    $('#login_vocde').on('click', changeVcod);
    $('#js-clear').on('click', function(){
        $('#js-username').val('');
        $('#js-password').val('');
        $('#js-code').val('');
    });
    
    window.addEventListener("message", receiveMessage, false);

    function receiveMessage(event)
    {
      if(event.data != null || event.data != undefined){
    	  errorAndshowCode(event.data,false);
      }
    }
    
    // 优化 增加tab选中样式
    $('#js-login').on('focus', function(){
      $(this).css('outline', 'rgb(77, 144, 254) auto 5px');
    });
    $('#js-login').on('blur', function(){
      $(this).css('outline', 'rgb(109, 109, 109) none 0px');
    });
    $('#js-password').on('keyup', function(e){
      if(e && e.keyCode === 13) {
        loginFunction();
      }
    });
    $('#js-login').on('keyup', function(e){
        if(e && e.keyCode === 13) {
          loginFunction();
        }
      });
})();

