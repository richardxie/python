/**
 *  @Author:Beyond
 *  @version:1.0.0
 *  @deprecated 弹出层提示插件
 * 
 * ***/
(function() {
	$.extend({
		idialog: {
			close: function() {
				$("#idialog_confirm,#idialog_cancel,#but_close1").unbind("click");
				$("#idialog_window,#idialog_overlay").remove();
				if (typeof document.body.style.maxHeight == "undefined") {
					$("body", "html").css({
						height: "auto",
						width: "auto"
					});
				}
			},
			_fixedHeight: function(overlay_height) {
				$("#idialog_window").css({"top":(overlay_height - $("#idialog_window").height()) / 2 + $(document).scrollTop()});
			}, 
			show: function(arg, callback) {
				var dialogWidth = arg.width != undefined ? arg.width: 300;
				var dialogTitle = arg.title != undefined ? arg.title: "提示信息";
				var msg = arg.msg != undefined ? arg.msg: "";
				if(msg.length>20&&arg.width == undefined)
				{dialogWidth=600;}
				var dialogHeight = arg.height != undefined ? arg.height: 100;
				var need_btn = arg.showButton == undefined ? true: false;
				var msg_type = "";
				var msg_style=arg.className!=undefined?" class="+arg.className:"";
				var delay=arg.delay!=undefined?arg.delay:2;
				var msg_location=arg.location!=undefined?arg.location:false;
				var mask = arg.showMask == undefined ? " class=mask": "";
				var autoClose=arg.autoClose == undefined ?false:true;
				var okBtn=arg.okBtn== undefined ? "<button class=\"button02\"  type='button' id='idialog_confirm'>确定</button>" : arg.okBtn;
				var cancelBtn="&nbsp;<button class=\"button02\"  type='button' id='idialog_cancel'>取消</button>";
				var btn=okBtn;
				switch (arg.icon) {
				case "ok":
					msg_type = "probox8";
					break;
				case "warning":
					msg_type = "probox9";
					break;
				case "faild":
					msg_type = "probox10";
					break;
				case "normal":
					msg_type = "probox11";
					break;
				case "confirm":
					msg_type = "probox14";
					btn=btn+cancelBtn;
					break;
				}
				//loadding url 显示加载动画
				if (arg.url) {
					msg_type = "probox12";
				}
				//添加背景层,前提是不存在
				if ($("#idialog_overlay").length) {
					$("#idialog_overlay,#idialog_window").remove();
				}
					$("body").append("<div id='idialog_overlay' " + mask + "></div>"); //添加窗口
					$("body").append("<div id=idialog_window class='probox13'></div>");
					var idialog_html = "";
					if (arg.icon == "loading") {
						 
						idialog_html = "<div class=\"probox\" ><div class=\"probox7\"  style=' text-align:center;height:" + dialogHeight + "px;line-height:" + dialogHeight + "px; ' > <p class=\"probox12 "+msg_style+"\" style='display:inline;padding-left:20px;float:none'>"+ arg.msg + "</p></div>	 </div>";
					} else {
						idialog_html += "<div class=\"proboxcir\">";
						idialog_html += "<div class=\"probox7\">";
						idialog_html += "<div class=\"probox1\">";
						idialog_html += "<p>" + dialogTitle + "</p>";
						idialog_html += "<span class=\"probox4\" name=\"but_close\"  id=\"but_close1\" title='按ESC键也可以关闭'></span>";
						idialog_html += "</div>";
						idialog_html += "<div class=\"probox2 "+msg_style+"\">";
						idialog_html += "<b class='" + msg_type + "'></b>" + msg;
						idialog_html += "</div>";
						if (need_btn) {
							idialog_html += "<div class=\"probox3\">"+btn+"</div>"; 
						}
						idialog_html += "</div>";
						idialog_html += "</div>";
					}
					$("#idialog_window").append(idialog_html);
					//自动关闭
					if(autoClose){
						setTimeout(function(){$.idialog.close(); },delay*1000)
					}
					//绑定方法，移除对话框
					$("#idialog_confirm,#idialog_cancel,#but_close1").bind("click",
					function() {
						$.idialog.close();

					});
					//绑定回调函数
					if (typeof(callback) != "undefined") {
						$("#idialog_confirm").unbind("click").bind("click",
						function() {
							if (callback()) {
								$.idialog.close();
							}
						});
						$("#idialog_cancel,#but_close1").unbind("click").bind("click",
						function() {
							$.idialog.close();
						});
					}

					var overlay_w = $(window).width();
					var overlay_h = $(window).height();
					//计算绝对位置并显示对话框
					if (dialogWidth) {
						$("#idialog_window").css("width", dialogWidth + "px");
					}
					var sd_top = (overlay_h - dialogHeight) / 2 + $(document).scrollTop();
					sd_top = sd_top < 0 ? 0 : sd_top;
					var sd_left = (overlay_w - $("#idialog_window").width()) / 2;
					sd_left = sd_left < 0 ? 0 : sd_left;

					$("#idialog_window").css({
						"left": sd_left,
						"position": "absolute",
						'padding': "8px",
						'z-index': 5000,
						"width": dialogWidth,
						"min-height": dialogHeight + "px",
						"_height": dialogHeight + "px"
					}).show(function() {
						//从新计算高度 
						$.idialog._fixedHeight(overlay_h);
						$(document).unbind("keyup").bind("keyup",function(e) {
							var key = e.keyCode;
							if (key == 27||key==13) {
                                if (typeof(callback) != "undefined") {
                                    callback();
                                }
                                $.idialog.close();
							}
						}); 
						if(msg_location!=	false){
							//跳转 
							setTimeout(function(){location.href=msg_location; },delay*1000)
						}
						//URL 延迟加载
						if (arg.url) {
							
							setTimeout(function() {
								$("#idialog_window .probox2").load(arg.url,
								function() {
									$.idialog._fixedHeight(overlay_h);
								});
							},
							arg.timeout >= 0 ? arg.timeout: 2000)
						}
					}).focus();
 
			}
		}
	})
})(jQuery);