/**
 * @uses 开心利是js文件
 * @author jhl
 */
$(document).ready(function(){
	var last_index=1;
	var right_move=-170;
	var left_move=170;
	var how_num=$(".wf_list_box").length;
	var how_much=$(".wf_list_lv").length;
	$(".wf_list_box").eq(1).css("margin-top","0px");
	if(how_much==3){		
		$(".wf_list_lv").eq(last_index).hide();
		$(".wf_xq_box").eq(last_index).show();
	}else if(how_much==2 || how_much==1){
		$(".wf_list_lv").eq(0).hide();
		$(".wf_xq_box").eq(0).show();
		last_index=0;
	}
	
	var move_jl=-600;
	$(".wf_move_box").animate({"margin-left":move_jl+"px"});
	$(".wf_list_lv").each(function(i){
		$(this).click(function(){
			$(".wfxq_cont2_up").hide();			
			$(".wf_bg_box").height("970px");
			$(".wf_xq_cont2").hide();
			$(".wfxq_cont1_down").show();
			$(".wf_list_lv").show();
			$(this).hide();
			$(".wf_xq_box").hide();
			$(this).next().fadeIn();
			$(".wf_list_box").css("margin-top","95px");
			$(this).parent(".wf_list_box").css("margin-top","0px");
			var move_index=i-last_index;
			move_jl=move_jl+move_index*right_move;
			if(how_num>1){
				if(i>last_index){
				$(".wf_move_box").animate({"margin-left":move_jl+"px"});	
					last_index=i;					
				}
				else if(i<last_index){
				$(".wf_move_box").animate({"margin-left":move_jl+"px"});	
					last_index=i;
				}
			}
		});
		
	});

	$(".wfxq_cont1_down").each(function(i){
		$(this).click(function(){
			$(this).hide();
		if($(".wf_xq_cont2").eq(i).height()>430){
			var  add_height=$(".wf_xq_cont2").eq(i).height()-430+1000;
			$(".wf_bg_box").height(add_height+"px");
		}
		$(".wfxq_cont2_up").eq(i).show();
		$(".wf_xq_cont2").eq(i).fadeIn();
		
		});	
	});
	
	$(".wfxq_cont2_up").each(function(i){
		$(this).click(function(){
			$(this).hide();			
			$(".wf_bg_box").height("970px");
			$(".wf_xq_cont2").eq(i).hide();
			$(".wfxq_cont1_down").eq(i).show();
		});
	});
	//提示框的居中
	var wf_width=$(".wf_ts_txt").outerWidth();
  	var wf_width="-"+(wf_width/2+"px");
  	$(".wf_ts_txt").css("margin-left",wf_width);
	
	
	//进度条
	$(".pie_circle").each(function(i){
		var pie_num=$(this).find("span").html();
			pie_num=Math.floor(pie_num);
			if (pie_num > 79) {
				$(this).css("background-color", "#b52026");
			}
			var jd=Number(pie_num* 3.6);
		if (jd <= 180) {
			$(this).find('.pie_right2').css('transform', "rotate(" + jd + "deg)");
		} else {
			$(this).find('.pie_right2').css('transform', "rotate(180deg)");
			$(this).find('.pie_left2').css('transform', "rotate(" + (jd - 180) + "deg)");
		}
	});
	
	//输入金融获取焦点
	$(".amountt_input").on('input',function(e){
		var ibid = $(this).attr('dataid');
		$("#savehbid_"+ibid).val("");
		$("#savehbje_"+ibid).val("");
		$(".yebz_ts_"+ibid).html("");
	});
	
	//输入金融失去焦点
	$('.amountt_input').blur(function() {
		var ibid = $(this).attr('dataid');
		var value = $(this).val();
		value = value.replace(/[^\d.]/g,""); //清除"数字"和"."以外的字符
		value = value.replace(/^\./g,""); //验证第一个字符是数字而不是
		value = value.replace(/\.{2,}/g,"."); //只保留第一个. 清除多余的
		value = value.replace(".","$#$").replace(/\./g,"").replace("$#$",".");
		value = value.replace(/^(\-)*(\d+)\.(\d\d).*$/,'$1$2.$3'); //只能输入两个小数
		value = Math.floor(value);
		$(this).val(value);
		 if (value >= 50) {
			$.ajax({
				type:'POST',
				data:{iborrid:ibid,amoutval:value},
				url:"/Invest/getIncome",
				dataType:"json",
				success: function(data){
						if(data.status!=1){
							$.idialog.show({
								icon: 'normal',
								title: '系统提示',
								msg:data.info
							});
						}else{
							/**/
							get_sy(data,ibid);
						}
					}
				})
			}
	});
	
    //关闭弹窗
	$('.icon-close').click(function() {
		var ibid = $(this).attr('dataid');
		$('#coninvest_'+ibid).hide();
		$('#incheck_'+ibid).removeAttr('disabled');
	});
	
	//最大可投
	$('.mostaccount2_max').click(function() {
		var ibid = $(this).attr('dataid');
		$("#savehbid_"+ibid).val("");
		$("#savehbje_"+ibid).val("");
		var zhye = parseFloat(UI.Money($('#zhkyye_'+ibid).val()));
		var hxjk = parseFloat(UI.Money($('#hxjk_'+ibid).val()));
		var zdtbe = parseFloat(UI.Money($('#zdtbe_'+ibid).val()));
		var maxje=0;
		if(isNaN(zdtbe)) {
				maxje=hxjk;
		}else{
			if(zdtbe<hxjk){
				maxje=zdtbe;
			}else{
				maxje=hxjk;
			}
		}
		if(document.getElementById("ktmje_"+ibid)){
			var ktmje=Number($("#ktmje_"+ibid).val());
			if(ktmje<50){
				return false;
			}else{
				if (maxje < ktmje){
					maxje=Math.floor(maxje);
					$('#amountt_'+ibid).val(maxje);
				}
				else{
					ktmje=Math.floor(ktmje);
					$('#amountt_'+ibid).val(ktmje);
				}
			}
		}else{
			if (maxje < zhye){
				maxje=Math.floor(maxje);
				$('#amountt_'+ibid).val(maxje);
			}
			else{
				zhye=Math.floor(zhye);
				$('#amountt_'+ibid).val(zhye);
			}
		}
			$.ajax({
			type:'POST',
			data:{iborrid:$("#ibid_"+ibid).val(),amoutval:$("#amountt_"+ibid).val()},
			url:"/Invest/getIncome",
			dataType:"json",
			success: function(data){
					if(data.status!=1){
						$.idialog.show({
							icon: 'normal',
							title: '系统提示',
							msg:data.info
						});
					}else{
						get_sy(data,ibid);				
					}
				}
			})
	});
	
	//点击立即投资
    $(document).on('click','.button_confirm_invest',function(){
		var ibid = $(this).attr('dataid');
		button(ibid);
    });
  //投资
    $('.incheck_now').click(function() {
    	var ibid = $(this).attr('dataid');
    	var syje=Number($("#hxjk_"+ibid).val());
    	var zxtbe=Number($("#zxtbe_"+ibid).val());
    	var zdtbe=$("#zdtbe_"+ibid).val();
    	var ktmje=Number($("#ktmje_"+ibid).val());
    	if(zdtbe!="无限制"){
    		zdtbe=Number(zdtbe);
    	}

    	var zhkyye=Number($("#zhkyye_"+ibid).val());

    		if (!$('#amountt_'+ibid).val()){
    			$(".yebz_ts_"+ibid).html("请输入投资金额,投资金额必须大于50！");
    	 		return false;
    		}else{

    			if(Number($('#amountt_'+ibid).val())>zhkyye){
    				$(".yebz_ts_"+ibid).html("余额不足，请先去充值吧！");
    				return false;
    			}

    			if(Number($('#amountt_'+ibid).val())>ktmje){
    				$(".yebz_ts_"+ibid).html("可投开心利是金额不足，请先去充值吧！");
    				return false;
    			}
    			
    			if(syje>zxtbe){
    				//剩余金额大于最小可投金额时
    				if (Number($('#amountt_'+ibid).val())<50){
    					$(".yebz_ts_"+ibid).html("投资金额必须大于50元");
    	 				return false;
    				}
    				if(zdtbe!="无限制"){
    					if(Number($('#amountt_'+ibid).val())<zxtbe || Number($('#amountt_'+ibid).val())>zdtbe){
    						$(".yebz_ts_"+ibid).html("投资必须大于"+zxtbe+"元小于"+zdtbe+"元");
    		 				return false;
    					}
    				}else{
    					if(Number($('#amountt_'+ibid).val())<zxtbe){
    						$(".yebz_ts_"+ibid).html("投资必须大于"+zxtbe+"元");
    		 				return false;
    					}
    				}
    				if(Number($('#amountt_'+ibid).val())>syje){
    					$(".yebz_ts_"+ibid).html("超出剩余可投金额！");
    		 				return false;
    				}
    			}else{
    				//剩余金额小于最小可投金额时
    				if (Number($('#amountt_'+ibid).val())<50){
    					$(".yebz_ts_"+ibid).html("投资金额必须大于50元");
    	 				return false;
    				}
    				if(zdtbe!="无限制"){
    					if(Number($('#amountt_'+ibid).val())<zxtbe || Number($('#amountt_'+ibid).val())>zdtbe){
    						$(".yebz_ts_"+ibid).html("投资必须大于"+zxtbe+"元小于"+zdtbe+"元");
    		 				return false;
    					}
    				}else{
    					if(Number($('#amountt_'+ibid).val())<zxtbe){
    						$(".yebz_ts_"+ibid).html("投资必须大于"+zxtbe+"元");
    		 				return false;
    					}
    				}	
    			}
    		}
    	
    	$.ajax({
    		dataType: 'json',
    		url: '/Invest/investcheck/ibid/' + ibid,
    		beforeSend: function() {
    			$('#incheck_'+ibid).html('检查是否可投中...')
    		},
    		success: function(data) {
    			if(data.status==503){
    					$(".loginbtn_"+ibid).trigger("click");	
    			}else{
    				if(data.status==129){
    					
    					if($("#sf_span_"+ibid).html()!=null && $("#sf_span_"+ibid).html()!=""){
    						$(".earnings_"+ibid).eq(1).html("实付: "+$("#sf_span_"+ibid).html());
    					}
    					$('#coninvest_'+ibid).show();
                         popcenterWindow('#coninvest_{$iborrow_info.id} #animate_'+ibid);//弹窗居中
    					$('#amount_money_'+ibid).html($('#amountt_'+ibid).val());
    					$('#incheck_'+ibid).html('立即投资')
                        var yy = document.getElementById("ppay_"+ibid);
                        yy.value="";
                        yy.focus();
    					 $('#cinvest_'+ibid).show();
    					$('#cancel2_{$iborrow_info.id},#cinvest_'+ibid).click(function() {
    						$('#coninvest_'+ibid).hide();
    						$('#amounto_{$iborrow_info.id},#amountt_{$iborrow_info.id},#ppay_{$iborrow_info.id},#sendnumber_'+ibid).val(''); 
    						$('#amountoTip_'+ibid).html('');
    					});
    					var amounto = $('#amounto_'+ibid).val();
    					if (amounto != '') {
    						$('#amountt_'+ibid).attr('value', amounto);
    					}
    				}else if(data.status==503){
    					location.href="/NewLogin";
    				}else{
    					$('#incheck_'+ibid).html('立即投资');
    					$.idialog.show({
    						icon: 'normal',
    						title: '系统提示',
    						msg: data.info
    					});
    					return false; 
    				} 
    			}
    			 
    		}
    	});
    });
    
    //输入金融按下回车进行投资
    $(".ppay_input_data").bind('keydown',function(event){
    	var ibid = $(this).attr('dataid');
    	var e = event || window.event;
    	if(!e.ctrlKey && e.keyCode ==13){
    		button(ibid);
    		return false;
    	}
    });
    
    
});


function get_sy(data,ibid){
	$("#yj_span_"+ibid).html("预计收益:&nbsp;&nbsp;&nbsp;￥" + data.info);
		if($("#hbje_span_"+ibid).html()!=""){
			var sf=Number($("#amountt_"+ibid).val())-Number($("#savehbje_"+ibid).val());
				sf=sf.toFixed(2);
			$("#sf_span_"+ibid).html("￥" + sf);
		}else{
			$("#sf_span_"+ibid).html("￥" + $("#amountt_"+ibid).val());
		}
	 $(".interest_t_"+ibid).html("￥"+data.info).fadeIn().next('b').show();
}

//投资
function button(ibid){
	if ($("#button_"+ibid).val() == '正在投资..') {
		return;
	}
	$('#ppay_error_'+ibid).addClass('none')
	 var ibid = $('#ibid_'+ibid).val();
	//var ppay = $('#ppay_'+ibid).val();
	var ppay = $('#ppay_'+ibid).val();
	ppay = encode64(xxtea_encrypt(utf16to8(ppay), $("#uniqKey").val()))
	var iborrownumid = $('#iborrownumid_'+ibid).val();
	var amountt = $('#amountt_'+ibid).val();
	var lunchid = 0;
	if($("#savehbid_"+ibid).val()!=""){
		lunchid = $("#savehbid_"+ibid).val();
	}
	if (!amountt) {
		$("#uiviewmsg_"+ibid).html("<font>可投金额未填写</font>");
	 
		return false;
	}
	if (!ppay) {
		$('#uiviewmsg_'+ibid).html('<font color=\'red\'>交易密码未填写</font>');
	} else {
		//var userid = "{$user_id}";
		$.ajax({
			type: 'POST',
			dataType:"json",
			url: '/Invest/checkppay', 
			beforeSend: function() {
				$('#button_'+ibid).val('正在投资..')
			},
			data: {
				p_pay: ppay,
				//user_id: userid,
				ibnum: iborrownumid,
				lunchId:lunchid,
				amount: amountt,
                '__hash__':$("input:hidden[name=__hash__]").val()
			},
			cache: false,
			success: function(data) { 
				if(data.status==0){
					window.location.href="/NewLogin";
				}else if (data.status == 155){
					$("#uiviewmsg_"+ibid).html("<font color=red>"+data.info+"</font>");
					$('#button_'+ibid).val('确认投资');
				}
				else if (data.status == 119) { 
                      $(".queue-box_"+ibid).fadeIn(600);
                      var tnum = data.tnum;
                      var borrow_num = $("#iborrownumid_"+ibid).val();
                      timer(16, borrow_num, tnum,ibid);                 
				} else if (data.status == 118) {
					$('#button_'+ibid).val('确认投资')
					 $('#coninvest_'+ibid).hide();
					   $.idialog.show({icon:   "info" , msg: data.info });  
				} else if (data.status == 117) {
					$('.invest_mb_'+ibid).removeClass('none');
				} else if (data.status == 101||data.status==102) {
					$('#button_'+ibid).val('确认投资')
					 $('#ppay_error_'+ibid).removeClass('none').find('span').html(data.info)
					 $(this).val('确认投资');
				}else if(data.status==200){
					$("#showinfo_"+ibid).html(data.info);
                    if(data.status==119){
                         window.location.href="/Invest/done";
                    }else{
                        $("#showinfo_"+ibid).html(data.info); 
                    }
				 
				 
				}else if(data.status==203){
					$("#showinfo_"+ibid).html(data.info);
					$('#button_'+ibid).val('重投'); 
				} else { 
						 $("#uiviewmsg_"+ibid).html("<font color=red>"+data.info+"</font>"); 
						$('#button_'+ibid).val('重投'); 
				}
			},
			error: function(xhr, status, text) {
				console.log({xhr:xhr,status:status,text:text});
				$('#button_'+ibid).val('重投');
			}
		});
	}
}

function password_v(val,ibid) {
    if (val.length >= 1) {
        //document.all.suretender.disabled=false; button-red
        $("#button_"+ibid).attr("disabled", "");
        $("#button_"+ibid).attr("disabled", false);
        $("#button_"+ibid).removeClass("button-gray");
        $("#button_"+ibid).addClass("button-red");
    } else {
        //document.all.suretender.disabled=true;
        $("#button_"+ibid).attr("disabled", true);
        $("#button_"+ibid).removeClass("button-red");
        $("#button_"+ibid).addClass("button-gray");
    }
}

//弹窗水平居中
function popcenterWindow(divID){
    var windowWidth=$(window).width(); //获得窗口的宽度 
    var popWidht=$(divID).width();//获得弹窗的宽度 
    var popX=(windowWidth-popWidht)/2;  
    $(divID).css({'left':popX,'z-index':4});
}

//投资队列倒计时
function timer(defSec,borrow_num,tnum,ibid) { 
	defSec=defSec<=15&&defSec>=0?defSec:15; 
	$(".queue-time_"+ibid).html(defSec--);  
	if(defSec < 0){
        ///15秒结束
        window.location.reload();
	}else{
        if( defSec % 3 == 0){
            ////每隔15秒到后台轮询。
            getData(borrow_num,tnum,ibid);
        }
		window.timeOut = window.setTimeout("timer("+defSec+ ",'" + borrow_num + "','" + tnum + "','" + ibid + "')",1000);
	} 
 }

//投资成功后处理
function getData(borrow_num,tnum,ibid){
    /////获取后台数据，并更新。
    $.ajax({
        url:"/Public/tenderinfo",
        type:"Post",
        dataType:"json",
        data:{borrow_num:borrow_num,tnum:tnum},
        success:function(data){
              /////成功，更改状态，操作
            if(data.status){  
                window.location.href = "/Invest/done";
            }else{
                if(data.data && data.info){
                    $(".queue-box_"+ibid).find(".p1").html(data.info.info);
                    clearTimeout(window.timeOut);
                    setTimeout(function(){
                        window.location.reload();
                    },3000);
                }else{
                    ///////可能还没处理到这个列项。
                }
            }
            
        }
    });
}

//开心利是倒计时
function queue_timer(defSec) { 
	$(".wf_queue_time").html(defSec--);
	if(defSec < 0){
    window.location.href="/";
	}else{
	window.timeOut = window.setTimeout("queue_timer("+defSec+")",1000);
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
				 str_time +=  int_hour + ':' + int_minute + ':' + int_second;
	    timer.text(str_time);
	    var self = this;
	    setTimeout(function () {
	      self.setTimeShow();
	    }, 1000);
	    //D:正确 
	  } else {
	    timer.text('投资已满或过时');
	    return ;
	  }
	}

	function getAccountInfo(ibid) {
		var that = this;
		$.ajax({
			'type': 'GET',
			'dataType': 'json',
			url: '/Invest/getAccountInfo',
			beforeSend: function(){$(".refreshbtn_"+ibid).removeClass('icon-refalsh').addClass('icon-loadding')},
			success: function(data) {
				if (data.status == 1) {
					$('#zhkyye_'+ibid).val(data.money);
					$('.formated_zhkyye_'+ibid).html('￥' + data.formated_money);
				}else{
					$(".loginbtn").trigger("click");	
				}
				$(".refreshbtn_"+ibid).removeClass('icon-loadding').addClass("icon-refalsh");
			}
		})
	}

 $(function(){
 var $xm_li=$(".wfxq_cont2_title  li");
 $xm_li.click(function(){
	$(this).addClass("wfxq_xl_on")
	        .siblings().removeClass("wfxq_xl_on");
			var index=$xm_li.index(this);
			$(".wfxq_txt_content>div") 
			              .eq(index).show()
						  .siblings().hide();
 });	
 });
 
 ///////开心利是分页控制////////
	/**
	 * 开心利是投资页面请求数据主体
	 */
	function IborrowTenderFirstReqDate(){
		//传送的数据
		var obj = {};
		obj.id = $('input[name=id]').val();
		obj.goto_page = $('input[name=goto_page]').val();
		obj.page_href = $('input[name=page_href]').val();
		return obj;
	}
	
	/**
	 * 开心利是投资列表
	 */
	function IborrowTenderWelfareModel(pdata){
		 var backhtml='';
		 //1:网站自动,2:网站手动,3:移动端
		 $.each(pdata,function(index,item){
			 var classstype = 0;
			 if(item.type == 1){
				 classstype = 'zdtz_icon'; 
			 }else if(item.type == 2){
				 classstype = 'pc_icon'; 
			 }else if(item.type == 3){
				 classstype = 'app_icon'; 
			 }else if(item.type == 4){
				 classstype = 'app_icon';
			 }
			 backhtml +='<li>';
          backhtml +='	<span class="wfxq_xmjl_time">'+item.addtime+'</span>';
          backhtml +='	<span class="wfxq_xmjl_name">'+item.username+'</span>';
          backhtml +='	<span class="wfxq_xmjl_money">￥'+item.account+'</span>';
          backhtml +='	<span class="wfxq_xmjl_icon '+classstype+'"></span>';
          backhtml +='</li>';  
		 });
		 return backhtml;
	}
 
	/**
	 * @uses 列表请求接口
	 * @author jhl
	 * @return json
	 */
	function getListDatas(id){
		//获取请求数据
		//传送的数据
		var obj = {};
		obj.id = id;
		obj.goto_page = $('.page_box_show_'+id).find('.goto_page').val();
		obj.page_href = $('input[name=page_href_'+id+']').val();
		//开始请求数据
		$.ajax({
			type:"POST",
			dataType:"json",
			url:'/Invest/getIborrowTenderList',
			data:obj,
			beforeSend:function(){
				 $('.wfxq_xmjl_neirong_'+id).html('<div style="text-align:center;margin:60px 0px 0px 0px;"><img class="ajax_loader" src="/Public/Images/ajax-loader.gif" /></div>');
			},
			success:function(data){
				if(data.status > 0 && data.list.length > 0){
					 $('.wfxq_xmjl_neirong_'+id).html(IborrowTenderWelfareModel(data.list));
					 $('.page_box_show_'+id).html(data.page);
				}else{
					$('.wfxq_xmjl_neirong_'+id).html('');
					$('.page_box_show_'+id).html('');
				}
			},
			error:function(){
			    $.idialog.show({
			        icon: 'normal',
			        title: '请求错误',
			        msg: '请求错误'
			    });
			}
		});
	}
 
	//分页
    $(document).on("click",".page_box ul li a",function(){
    	var ibid = $(this).parent().parent().parent().parent().attr('ibid');
		var href = $(this).attr('href');
        if(href == ""){
            return false;
        }
    	$('input[name=page_href_'+ibid+']').val(href);
        getListDatas(ibid);
        return false;
    });
    
	//跳转到指定页面事件
    $(document).on("click",".page_btn",function(){
    	var ibid = $(this).parent().parent().parent().parent().attr('ibid');
        var goto_page = $('.page_box_show_'+ibid).find('.goto_page').val();
        if(goto_page == ""){
            return false;
        }
        //清除page_href
        $('input[name=page_href_'+ibid+']').val('');
        getListDatas(ibid);
    });
    
	//点击开心利是投资记录
	$(document).on('click', '.wfxq_tzjl_title', function() {
			var obj = {};
			obj.id = $(this).attr('ibid');
			obj.goto_page = $('input[name=goto_page_'+obj.id+']').val();
			obj.page_href = $('input[name=page_href_'+obj.id+']').val();
			//开始请求数据
			$.ajax({
				type:"POST",
				dataType:"json",
				url:'/Invest/getIborrowTenderList',
				data:obj,
				beforeSend:function(){
					 $('.wfxq_xmjl_neirong_'+obj.id).html('<div style="text-align:center;margin:60px 0px 0px 0px;"><img class="ajax_loader" src="/Public/Images/ajax-loader.gif" /></div>');
				},
				success:function(data){
					if(data.status > 0 && data.list.length > 0){
						 $('.wfxq_xmjl_neirong_'+obj.id).html(IborrowTenderWelfareModel(data.list));
						 $('.page_box_show_'+obj.id).html(data.page);
	 
						 //执行操作
						var $xm_li = $(".wfxq_cont2_title  li");
						$(this).addClass("wfxq_xl_on").siblings().removeClass("wfxq_xl_on");
						var index = $xm_li.index(this);
						$(".wfxq_txt_content>div").eq(index).show().siblings().hide();
						var li_height = data.list.length * 47;
						var height = $(".wf_xq_cont2").height()* 1 + li_height;
						if (height > 430) {
							var add_height = $(".wf_xq_cont2").height() - 430 + 1000;
							$(".wf_bg_box").height(add_height + "px");
						}
						 
					}else{
						$('.wfxq_xmjl_neirong_'+obj.id).html('');
						$('.page_box_show_'+obj.id).html('');
					}
				},
				error:function(){
				    $.idialog.show({
				        icon: 'normal',
				        title: '请求错误',
				        msg: '请求错误'
				    });
				}
			});

	});
 
 
 
 
 
 
 
 
 
 
 
 