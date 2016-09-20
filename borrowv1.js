//倒计时
function timer(defSec,borrow_num,tnum) { 
	defSec=defSec<=15&&defSec>=0?defSec:15; 
	$(".queue-time").html(defSec--);  
	if(defSec < 0){
        ///15秒结束
        window.location.reload();
	}else{
        if( defSec % 3 == 0){
            ////每隔15秒到后台轮询。
            getData(borrow_num,tnum);
        }
		window.timeOut = window.setTimeout("timer("+defSec+ ",'" + borrow_num + "','" + tnum + "')",1000);
	} 
 }
function getData(borrow_num,tnum){
    /////获取后台数据，并更新。
    $.ajax({
        url:"/Public/tenderinfo",
        type:"Post",
        dataType:"json",
        data:{borrow_num:borrow_num,tnum:tnum},
        success:function(data){
                        /////成功，更改状态，操作
            if(data.status){  
                window.RefalshTB(false);
                window.location.href = "/Invest/done";
            }else{
                if(data.data && data.info){
                    $(".queue-box").find(".p1").html(data.info.info);
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

function tabchange(obj, p) {
	$('#inv-hall-list01').attr('id', null);
	$(obj).find('span').attr('id', 'inv-hall-list01');
	ViewList(p);
}
function ViewList(pmode) {
	var modetype = pmode;
	var data;
	var url;
	if (pmod == 1) {
		data = {
			ib_id: $('#ibid').val()
		};
		url = '/Invest/detailed';
	}
	if (pmod == 2) {
		data = {
			user_id: $('#uid').val()
		};
		url = '/Invest/userinfo';
	}
	if (pmod == 3) {
		data = {
			user_id: $('#uid').val()
		};
		url = '/Ajax/preview';
	}
	if (pmod == 4) {
		data = {
			user_id: $('#uid').val()
		};
		url = '/Ajax/dataAppraisal';
	}
	$.ajax({
		type: 'POST',
		url: url,
		data: data,
		success: function(data) {
			$('#observer').html(data);
		}
	});
}
function getAccountInfo() {
	$.ajax({
		'type': 'GET',
		'dataType': 'json',
		url: '/Invest/getAccountInfo',
		beforeSend: function(){$(".refreshbtn").removeClass('icon-refalsh').addClass('icon-loadding')},
		success: function(data) {
			if (data.status == 1) {
				$('#zhkyye').val(data.money);
				$('.formated_zhkyye').html('￥' + data.formated_money);
			}else{
				$(".loginbtn").trigger("click");	
			}
			$(".refreshbtn").removeClass('icon-loadding').addClass("icon-refalsh");
		}
	})
}
$(document).ready(function() { 

    	var RefalshTB = window.RefalshTB = function(pisview) {
		var tpage = {
			'page': 1,
			'size':10
		};
		if (pageLYobj) {
			tpage = pagetdobj.GetParams();
		}
	 
		$.ajax({
			type: 'POST',
			url: cpath + '/GettbList',
			beforeSend: function(){ 
				$("#divtender").html("<div align=center><img src='/Public/Images/ajax-loader.gif' /></div>");
				},
			data: {
				tpage: tpage,
				ibnum: $('#iborrownumid').val()
			},
			success: function(data) {
				 
				if (data.status == 1) {
					backdatatoTBview(data.data, pisview, tpage);
					$('#incheck').removeAttr('disabled');
				} 
			}
		});
	}
	
	
    
    
		$(".media-body").live('mouseover mouseout',function(){ 
			 $('.media-reply',this).css({display:event.type == 'mouseover'?'block':"none"}) 
			} )	
			$(".interest").hide();
			$("#detai_nav A").click(function(){
				 $("#detai_nav A").removeClass('active');
				 $(this).addClass("active");
			})
	
		$("#confirm_edit").click(function(){
			$("#amountt2,#amountt").val($("#amountt2").val())
			$("#amount_money").html($("#amountt2").val());
			$('.inv-por7').addClass('none')
			$("#amount_money").parent().show();
			})
		$("#loginbtn").click(function(){ 
		$("#login_div").removeClass('none');
		})
		
  
 
 	$("#amount_money").click(function(){
			$(this).parent().hide();
			var v=$(this).html(); 
		 	$('.inv-por7').removeClass('none').find("input[type=text]").val(v);
			
			} );
			
	$("#animate").bind('click',showHiheInput);	
		$("#amountt2,#input2,#mostaccount").bind('click',stopBubble);
		
		function showHiheInput(){
			$("#showmoney").show();
			$('.inv-por7').addClass('none')
		}
		
	 
			
		//阻止事件冒泡函数
		function stopBubble(e){   
		    if (e && e.stopPropagation)  
		        e.stopPropagation()  
		    else  
		        window.event.cancelBubble=true  
		}
		
 
/*	$(".replay").live('click',function(){
		var comment_id=$(this).attr('inid'); 
	 
		var content=$(this).prev("textarea").val();
			 $.ajax({
				 type:'POST',dataType:"json",data:{id:comment_id,content:content},url:"/Invest/replay",success: function(data){
					 	if(data.status){
							RefalshLY();
							}else if(data.status==2){
								$(".loginbtn").trigger("click");	
							}else{
								$.idialog.show({ 	icon: 'normal', title: '系统提示', msg: data.msg }); 
							}
					 
					 }
				 })
	})*/
	
	
	$('#cancel2,#cinvest').click(function() {
		$('#coninvest').hide();
		$('#incheck').removeAttr('disabled');
	})
	 var lypagesize =10;
	var pageLYobj = null;
	var pagetdobj = null;
	var pagezrobj = null;
	function Creatpage() {
		pageLYobj = new UI.Page({
			toObj: $('#pagepanlly'),
			total: lytotal,
			size: lypagesize,
			star: 1,
			changepage: function(e1, e2, e3) {
			 
					RefalshLY();
			 
			}
		});
		pagetdobj = new UI.Page({
			toObj: $('#pagepanltd'),
			total: tdtotal,
			size: lypagesize,
			star: 1,
			changepage: function(e1, e2, e3) {
				RefalshTB();
			}
		});

		pagezrobj = new UI.Page({
			toObj: $('#pagepanlzrjl'),
			total: zrtotal,
			size: lypagesize,
			star: 1,
			changepage: function(e1, e2, e3) {
				RefalshZR();
			}
		});
		
	}
	Creatpage();
//	getlyAndtb();

		if(userId!="" && userId && userId==borrowUser){
				RefalshZR();
		}
	
	function getlyAndtb() {
		var tpage = {
			'page': 1,
			'size': lypagesize
		};
		if (pageLYobj) {
			tpage = pageLYobj.GetParams();
		}
		$.ajax({
			type: 'POST',
			url: cpath + '/Getlytb',
			beforeSend: function(){ 
				$("#divtender,#UIlylist").html("<div align=center><img src='/Public/Images/ajax-loader.gif' /></div>");
				},
			data: {
				tpage: tpage,
				ibnum: function() {
					return $('#iborrownumid').val();
				}
			},
			success: function(data) {
				if (data.status == 1) { 
					if(parseInt(data.data.ly.Total)){ 
						backdatatoLYview(data.data.ly, false, tpage); 
						}else{ 
							$("#UIlylist").html('');
						}
						if(parseInt(data.data.tb.Total)){
								backdatatoTBview(data.data.tb, false, {'page': 1,'size': lypagesize});
							}else{
							$("#divtender").html('');
						}
				
				} else {
					UI.showinfo('获得项目相关信息失败', 'warn');
				}
			}
		});
	}
	$('#movetotop').click(function() {
		var targetOffset = $('.header').offset().top;
		$('html,body').animate({
			scrollTop: targetOffset
		},
		800);
	});
	function backdatatoLYview(data, pisview, tpage) {
		
		if(!data.Total){
			return false;
			}
		Total = data.Total;
		startl = (Total - (tpage['page'] - 1) * tpage['size']);
		pageLYobj.settotal(Total, tpage['page']);
		if(data.Rows){
			BiudLYlist($('#UIlylist'), data.Rows, startl);
			}
		
		if (pisview != false) {
			var targetOffset = $('#lypos').offset().top;
			$('html,body').animate({
				scrollTop: targetOffset
			},
			800);
		}
	}
	function backdatatoTBview(data, pisview, tpage) {
		Total = data.Total;
		if(Total){
			
	
		startl = (Total - (tpage['page'] - 1) * tpage['size']);
		pagetdobj.settotal(Total, tpage['page']);
		BiudTBlist($('#divtender'), data.Rows, startl, data.status);
		//$('#lhtime').html(data.Total);
		$('.barvalue').html(data.bar + '%');
		$(".progressbar").css({"width":data.bar + '%'});
		if (pisview != false) {
			var targetOffset = $('#tbdiv').offset().top;
			$('html,body').animate({
				scrollTop: targetOffset-50
			},
			800);
		}
				}
	}
	
	/*转让记录*/
		function RefalshZR(pisview){
			var tmp="";
		var tpage = {
			'page': 1,
			'size':lypagesize
		};
		if (pagezrobj) {
			tpage = pagezrobj.GetParams();
		}
		
		$.ajax({
				type: 'POST',
			    url:"/Invest/getDebentureByBNum/",
			    dateType:"json",
			    data:{
			    		ibnum:ibnum,
			    		tpage:tpage
			         },
			        beforeSend: function(){ 
						$("#tab_attorn_table2").html('<tr><th colspan="7"><div align="center"><img  src="/Public/Images/ajax-loader.gif" /></div></th></tr>');
					},
			         success: function(data){
						 if(data.data.Total>0){
				         	for(var i=0;i<data.data.Rows.length;i++){
					         	tmp+='<tr>'
		                            +'<th>'+data.data.Rows[i].username+'</th>'		                     
		                            +'<th>'+data.data.Rows[i].buyer_name+'</th>'
		                            +'<th>￥'+data.data.Rows[i].principal+'</th>'
		                            +'<th>￥'+data.data.Rows[i].money+'</th>'
		                            +'<th>网站手动</th>'
		                            +'<th>'+data.data.Rows[i].success_time+'</th>'
									+'<th><a href="/Debenture/zrViewBorrow/id/'+data.data.Rows[i].id+'" target=\'_blank\'>查看</a></th>'
		                        	+'</tr>'
	                     	 }
								$("#tab_attorn_table2").html(tmp);
							 }else{
								  $("#tab_attorn_2").html("暂无转让记录");
							 }
			         },
			         error : function() { 
			         	alert("获取信息失败");
			         }

	});
	
}
	/*********/
	
	function RefalshLY(pisview) {
		var tpage = {
			'page': 1,
			'size': lypagesize
		};
		if (pageLYobj) {
			tpage = pageLYobj.GetParams();
		}
		$.ajax({
			type: 'POST',
			url: cpath + '/GetlyList',
			data: {
				tpage: tpage,
				ibnum: function() {
					return $('#iborrownumid').val();
				}
			},
			success: function(data) {
				if (data.status == 1) {
					backdatatoLYview(data.data, pisview, tpage);
				} else {
					UI.showinfo(data.info, 'warn');
				}
			}
		});
	}

	function BiudLYlist(obj, pdata, startl) {
		reval = '';
		$.each(pdata,
		function(index, item) {
			
 

			reval += '<div class="media">';
			reval += '  <a class="pull-left" href=\'/Account/MyNews/title/MMHPage/uid/' + item.guid + '\'>';
			reval += '<img class=\'media-object\' src=\'' + uimgpath + item.user_id + '/middle.jpg\' onerror=\'finddefuserimg($(this));\'/> ';
			reval += '    </a>';
			reval += '      <div class="media-body">';
			reval += '       <div class="media-heading"><a class="link-blue"  href=\'/Account/MyNews/title/MMHPage/uid/' + item.guid + '\'>' + item.username_mask + '</a></div>';
			reval += '      <div class="media-content">' + item.content + '</div>';
			reval += '        <div class="media-time">' + UI.timeFormat(item.addtime, 'yyyy-MM-dd hh:mm') + '</div>';
		/*	reval += "        					<!--点击“回复” 下面div加block-->";
reval += "        					<div class=\"media-reply\">";
reval += "        						<textarea class=rcontent>回复@"+ item.username_mask+"：</textarea>";
reval += "        						<input ibibid=\""+item.article_id+"\" inid='"+item.id+"' type=\"button\"  class='replay' value=\"回复\">";
reval += "        					</div>"; */
			reval += '     </div>';
			reval += '   </div>';
		});
		obj.html(reval);
		return true;
	};
	function comdify(thisobj)
	 {
		thisobj = thisobj.replace(/,/g, '');
		if (thisobj.length > 10)
		 {
			thisobj = thisobj.substring(0, 10);
		}
		var re = /\d{1,3}(?=(\d{3})+$)/g;
		var n1 = thisobj.replace(/^(\d+)((\.\d+)?)$/,
		function(s, s1, s2) {
			return s1.replace(re, '$&,') + s2;
		});
		return n1;
	} 
	function getType(thisobj) {
		var type = '';
		switch (thisobj) {
		case '1':
			type = '网站自动';
			break;
		case '2':
			type = '网站手动';
			break;
		case '3':
			type = '移动端';
			break;
		case '4':
			type = '微信端';
			break;
		}
		return type;
	}
	function BiudTBlist(obj, pdata, startl, status) {
		htmlstr = '';
		var userid = $('#userid').val();
		var uvpath = '/Account/MyNews/title/MMHPage/uid/';
		htmlstr += '<table class=\'tab-record-table\'>';
		htmlstr += '<tr class=\'inv-det5b6\'>';
		if (status == 1) {
			htmlstr += '<th class=\'inv-det5b1\'>序号</th> <th class=\'inv-det5b2\'  style="text-align:left">投资者</th> <th class=\'inv-det5b3\'  style="text-align:left">有效金额</th><th class=\'inv-det5b3\'  style="text-align:left">投资金额</th><th class=\'inv-det5b3\'  style="text-align:left">投资方式</th>   <th class=\'inv-det5b4\'  style="text-align:left">投资时间</th>';
		} else {
			htmlstr += '<th class=\'inv-det5b1\'>序号</th> <th class=\'inv-det5b2\'  style="text-align:left">投资者</th> <th class=\'inv-det5b3\'  style="text-align:left">有效金额</th><th class=\'inv-det5b3\'  style="text-align:left">投资金额</th>   <th class=\'inv-det5b4\'  style="text-align:left">投资时间</th>';
		}
		$.each(pdata,
		function(index, item) { 
			var current=item.user_id==$("#cuid").val()?"active":"";
			htmlstr += '<tr class="'+current+'"><td >';
			htmlstr += startl;
			htmlstr += '</td>';// ' <img   src=\'/Public/Images/' + item.icon +
			htmlstr += '<td  style="text-align:left">' + item.username_mask + '</td>';
			htmlstr += '<td style="text-align:left">￥' + comdify(item.account) + '</td>';
			htmlstr += '<td  style="text-align:left">￥' + comdify(item.money) + '</td>';
			if (status == 1) {
				htmlstr += '<td  style="text-align:left">' + getType(item.type) + '</td>';
			}
			htmlstr += '<td  style="text-align:left">' + UI.timeFormat(item.addtime, 'yyyy-MM-dd hh:mm:ss') + '</td>';
			htmlstr += '</tr>';
			startl -= 1;
		});
		htmlstr += '</tr>   </table>';
		obj.html(htmlstr);
		return true;
	}
	$('#RefalshLY').click(function() {
		RefalshLY();
	});
	$('#RefalshTB').click(function() {
		RefalshTB();
	});
	$("#confirm_edit").click(function(){
			$.ajax({
			type:'POST',
			data:{iborrid:$("#ibid").val(),amoutval:$("#amountt2").val()},
			url:"/Invest/getIncome",
			dataType:"json",
			beforeSend: function(){if($("#amountt2").val()<50){
				$("#uiviewmsg").html("<font color=red>投资金额需大于50</font>");
				
					return false;
				}},
			success: function(data){
					if(data.status!=1){
					  $("#uiviewmsg").html("<font color=red>"+data.info+"</font>");
					  var sfmoney=$("")
					  $(".earnings").eq(1).html("");
					}else{
						$("#uiviewmsg").html('点击按钮表示您同意支付投资金额');
						$('#amountt2').val($("#amountt2").val());
						//$(".interest").html("预计收益：<br />￥"+data.info).fadeIn().next('b').show();
                                                $(".interest_t").html("预计收益：￥"+data.info).fadeIn().next('b').show();
                                                if(data.continue_reward!=''){
                                                    $('.continue_reward').show().html(data.continue_reward);
                                                    $(".invest-det-show-b .earnings p").css('lineHeight','25px');
                                                    $('.invest-det-show-b .earnings .icon-question').css({'margin':'0','float':'none'});
                                                }else{
                                                    $('.continue_reward').hide();
                                                    $(".invest-det-show-b .earnings p").css('lineHeight','25px');
                                                    $('.invest-det-show-b .earnings .icon-question').css('margin','0');
                                                }
					}
					
				}
			})
	})
	$('#mostaccount2').click(function() {
		$("#hbje_span").html("");
		$("#savehbid").val("");
		$("#savehbje").val("");
		var zhye = parseFloat(UI.Money($('#zhkyye').val()));
		var hxjk = parseFloat(UI.Money($('#hxjk').val()));
		var zdtbe = parseFloat(UI.Money($('#zdtbe').val()));
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
		if(document.getElementById("ktmje")){
			var ktmje=Number($("#ktmje").val());
			if(ktmje<50){
				$(".yebz_ts").html("可投开心利是金额不足50元，请先去充值吧！");
				return false;
			}else{
				if (maxje < ktmje){
					$('#amountt').val(maxje);
				}
				else{
					$('#amountt').val(ktmje);
				}
			}
		}else{
			if (maxje < zhye){
				$('#amountt').val(maxje);
			}
			else{
				$('#amountt').val(zhye);
			}
		}

			$.ajax({
			type:'POST',
			data:{iborrid:$("#ibid").val(),amoutval:$("#amountt").val()},
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
						get_sy(data);				
					}
				}
			})
	 
	});
	$("#amountt").on('input',function(e){
		$("#hbje_span").html("");
		$("#savehbid").val("");
		$("#savehbje").val("");
		$(".yebz_ts").html("");
	});



	$('#amountt').blur(function() {
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
					data:{iborrid:$("#ibid").val(),amoutval:value},
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
								get_sy(data);
							}
						}
					})
				}
	});
	function ShowMsgdiv(ptitle, pmsg, purltext, purl) {
		$('#eee').html(ptitle);
		$('#wcon b').html(pmsg + '<br/>');
		$('#wcon span').addClass('orange acc-id24');
		$('#wcon a').addClass('link01');
		$('#wcon a').html(purltext);
		$('#wcon a').attr('href', purl);
		$('#aaa').show();
	}
	$('#closew').click(function() {
		$('#aaa').hide();
	});
	$('#incheck').click(function() {

		var syje=Number($("#hxjk").val());
		var zxtbe=Number($("#zxtbe").val());
		var zdtbe=$("#zdtbe").val();
		var ktmje=Number($("#ktmje").val());
		if(zdtbe!="无限制"){
			zdtbe=Number(zdtbe);
		}

		var zhkyye=Number($("#zhkyye").val());

			if (!$('#amountt').val()){
				$(".yebz_ts").html("请输入投资金额,投资金额必须大于50！");
		 		return false;
			}else{

				if(Number($('#amountt').val())>zhkyye){
					$(".yebz_ts").html("余额不足，请先去充值吧！");
					return false;
				}

				if(Number($('#amountt').val())>ktmje){
					$(".yebz_ts").html("可投开心利是金额不足，请先去充值吧！");
					return false;
				}
				
				if(syje>zxtbe){
					//剩余金额大于最小可投金额时
					if (Number($('#amountt').val())<50){
						$(".yebz_ts").html("投资金额必须大于50元");
		 				return false;
					}
					if(zdtbe!="无限制"){
						if(Number($('#amountt').val())<zxtbe || Number($('#amountt').val())>zdtbe){
							$(".yebz_ts").html("投资必须大于"+zxtbe+"元小于"+zdtbe+"元");
			 				return false;
						}
					}else{
						if(Number($('#amountt').val())<zxtbe){
							$(".yebz_ts").html("投资必须大于"+zxtbe+"元");
			 				return false;
						}
					}
					if(Number($('#amountt').val())>syje){
						$(".yebz_ts").html("超出剩余可投金额！");
			 				return false;
					}
				}else{
					//剩余金额小于最小可投金额时
					if (Number($('#amountt').val())<50){
						$(".yebz_ts").html("投资金额必须大于50元");
		 				return false;
					}
					if(zdtbe!="无限制"){
						if(Number($('#amountt').val())<zxtbe || Number($('#amountt').val())>zdtbe){
							$(".yebz_ts").html("投资必须大于"+zxtbe+"元小于"+zdtbe+"元");
			 				return false;
						}
					}else{
						if(Number($('#amountt').val())<zxtbe){
							$(".yebz_ts").html("投资必须大于"+zxtbe+"元");
			 				return false;
						}
					}	
				}
			}
		
		var ibid = $('#ibid').val();
		var bnum = $('#Bnum').val();
		$.ajax({
			dataType: 'json',
			url: cpath + '/investcheck/ibid/' + ibid,
			beforeSend: function() {
				$('#incheck').html('检查是否可投中...')
			},
			success: function(data) {
				if(data.status==503){
						$(".loginbtn").trigger("click");	
				}else{
					if(data.status==129){
						if($("#hbje_span").html()!=null ){
							if($("#hbje_span").html()!=""){
								$(".earnings").eq(0).html("红包: "+$("#hbje_span").html());
						}else{
								$(".earnings").eq(0).html("红包: 0 元");
						}	
					}
						if($("#sf_span").html()!=null && $("#sf_span").html()!=""){
							$(".earnings").eq(1).html("实付: "+$("#sf_span").html());
						}
						$('#coninvest').show();
                          popcenterWindow('#coninvest #animate');//弹窗居中
						$('#amount_money').html($('#amountt').val());
						$('#incheck').html('立即投资')
                                                 var yy = document.getElementById("ppay");
                                                 yy.value="";
                                                 yy.focus();
						 $('#cinvest').show();
						$('#cancel2,#cinvest').click(function() {
							$('#coninvest').hide();
							$('#amounto,#amountt,#ppay,#sendnumber').val(''); 
							$('#amountoTip').html('');
						});
						var amounto = $('#amounto').val();
						if (amounto != '') {
							$('#amountt').attr('value', amounto);
						}
					}else if(data.status==503){
						location.href="/NewLogin";
					}else{
						$('#incheck').html('立即投资');
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

                            //点击弹窗外空白处，关闭弹窗
							/*
                            document.onclick=function(){
								$(".hb_list_box").hide();
                                var e= window.event ? window.event: e,
								  target = e.srcElement || e.target;
                                while (target.nodeName.toLowerCase() != "html") {
                                       if(target.id=="animate"){ 
                                        break;
                                       }
                                        target = target.parentNode;
                                }
                                if(target.nodeName.toLowerCase()=="html"){
                             //      alert("点击了ID以外的元素");
                                   document.getElementById("coninvest").style.display = "none";
                             //      window.location.replace("/index/");
                                }else{
                                    document.getElementById("coninvest").style.display = "black";

                                }
								
                            }
							*/
                

	function showCantendErr(errnum) {
		switch (errnum) {
		case 1:
			ShowMsgdiv('检查是否登录', '您还没有的登录，不能进行投资！', '去网站登录吧 →', Loginurl);
			break;
		case 2:
			ShowMsgdiv('检查认证', '您还有未进行认证的项目，不能进行投资！', '去安全中心完善你的认证 →', Tosaft);
			break;
		case 3:
			ShowMsgdiv('检查交易密码', '您交易密码未设置，不能进行投资！', '去安全中心设置 →', Tosaft);
			break;
		case 4:
			ShowMsgdiv('检查账户余额', '账户余额为空，不能进行投资！', '去充值吧 →', '/Account/FundsManagement/title/Recharge');
			break;
		case 5:
			ShowMsgdiv('检查账户余额', '账户余额不足，不能进行投资！', '去充值吧 →', '/Account/FundsManagement/title/Recharge');
			break;
		case 6:
			ShowMsgdiv('检查是否是自己所发项目', '此项目是自己所发，不能进行投自己所发项目！', '请选择其它项目 →', '/Invest/index');
			break;
		case 7:
			ShowMsgdiv('检查项目密码', '项目密码错误，不能进行投资！', '', '#');
			break;
		case 8:
			ShowMsgdiv('错误', '无效项目', '请联系我们');
			break;
		default:
			ShowMsgdiv('错误', '未知错误', '请联系我们');
		}
	}
 
	$('#incheckpwd').click(function() {
		var ibid = $('#ibid').val();
		var bpwds = $('#bpwd').val();
		if(bpwds==""){
			$(".pwd_ts").html("请输入项目密码");
			return false;
		}
		$.ajax({
			dataType: 'json',
			async: true,
			type: 'POST',
			url: cpath + '/investcheckpwd/',
			data: {
				ibid: ibid,
				bpwdss: bpwds
			},
			beforeSend: function(){
				$("#incheckpwd").html("验证中....");
				},
			success: function(data) {
				if (data.status == 127 || data.status == 128) {
						$(".pwd_ts").html(data.info);
						$("#incheckpwd").html("重新验证");
				} else if (data.status==129) {
					$("#incheckpwd").html("验证正确...");
			  		location.reload();
				}else{
					$.idialog.show({
							icon: 'normal',
							title: '系统提示',
							msg: data.info
						});
				}
			}
		});
	});
	$("#bpwd").on('input',function(e){
		$(".pwd_ts").html("");
	});
	
	$('#feedback').click(function() {
		var editorss = $('#ibcontent').val();
		var userid = $('#cuid').val();
		var iborrownumid = $('#iborrownumid').val();
		if (userid == '') {
			$.idialog.show({
				icon: 'normal',
				title: '系统提示',
				msg: '您还没有登录！请登录之后再操作'
			});
		} else if (editorss == '') {
			$.idialog.show({
				icon: 'normal',
				title: '系统提示',
				msg: '留言内容不能为空'
			});
		} else {
			$.ajax({
				type: 'POST',
				url: '/Invest/feedback',
				data: {
					content: editorss,
					user_id: userid,
					ibnum: iborrownumid,
					r: 1
				},
				beforeSend: function() {
					$.idialog.show({
						icon: 'loading',
						msg: '留言保存中...'
					});
				},
				success: function(data) {
					if (data.status == 1) {
						 RefalshLY();
						 $('#ibcontent').val('');
						 $.idialog.close();
					} else {
						$.idialog.show({
							icon: 'normal',
							title: '系统提示',
							msg: data.info
						});
					}
					
				}
			});
		}
	});
                
        $("#button").bind('click',button);
        $("#ppay").bind('keydown',function(event){var e = event || window.event;if(!e.ctrlKey && e.keyCode ==13){button()}});
        
	function button(){
		if ($("#button").val() == '正在投资..') {
			return;
		}
		$('#ppay_error').addClass('none')
		 var ibid = $('#ibid').val();
		//var ppay = $('#ppay').val();
                 var ppay = encode64(xxtea_encrypt(utf16to8($("#ppay").val()), $("#uniqKey").val()));
		var iborrownumid = $('#iborrownumid').val();
		var amountt = $('#amountt').val();
		var lunchid = 0;
		if($("#savehbid").val()!=""){
			lunchid = $("#savehbid").val();
		}
		if (!amountt) {
			$("#uiviewmsg").html("<font>可投金额未填写</font>");
		 
			return false;
		}
		if (!ppay) {
			$('#uiviewmsg').html('<font color=\'red\'>交易密码未填写</font>');
		} else {
			var userid = userId;
			$.ajax({
				type: 'POST',
				dataType:"json",
				url: '/Invest/checkppay', 
				beforeSend: function() {
					$('#button').val('正在投资..')
				},
				data: {
					p_pay: ppay,
					user_id: userid,
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
						$("#uiviewmsg").html("<font color=red>"+data.info+"</font>");
						$('#button').val('确认投资');
					}
					else if (data.status == 119) { 
//                         //$.idialog.show({icon: "loading" , msg: data.info, location: '/Invest/done'});
                            
                                                //if($("#iborrowtype").val() == "5"){
                                                    $(".queue-box").fadeIn(600);
                                                    var tnum = data.tnum;
                                                    var borrow_num = $("#iborrownumid").val();
                                                    timer(16, borrow_num, tnum);
                                                /*}else{
                                                    RefalshTB(false);
                                                    window.location.href="/Invest/done";
                                                }*/
                                            
					} else if (data.status == 118) {
						$('#button').val('确认投资')
						 $('#coninvest').hide();
						   $.idialog.show({icon:   "info" , msg: data.info });  
					} else if (data.status == 117) {
						$('.invest_mb').removeClass('none');
					} else if (data.status == 101||data.status==102) {
						$('#button').val('确认投资')
						 $('#ppay_error').removeClass('none').find('span').html(data.info)
						 $(this).val('确认投资');
					}else if(data.status==200){
						$("#showinfo").html(data.info);
                        if(data.status==119){
                                RefalshTB(false);
                             window.location.href="/Invest/done";
                        }else{
                            $("#showinfo").html(data.info); 
                        }
					 
					 
					}else if(data.status==203){
						$("#showinfo").html(data.info);
						$('#button').val('重投'); 
					} else { 
							 $("#uiviewmsg").html("<font color=red>"+data.info+"</font>"); 
							$('#button').val('重投'); 
					}
				},
				error: function(xhr, status, text) {
					console.log({xhr:xhr,status:status,text:text});
					$('#button').val('重投');
				}
			});
		}
	};
        
        $("#getAccountInfo").click(function(){
			 location.reload();
		});
});

function checkhb(i,hbid,hbje,userConstraint){
		$(".hbcheck_1").html("");
		$(".hbcheck_1").eq(i).html('<div class="hbcheck_2"></div>');
		$("#savehbid").val(hbid);
		$("#savehbje").val(hbje);
		if($("#amountt").val()==""){
			$("#amountt").val(userConstraint);
		}
		$("#hbje_span").html($(".hb_me").eq(i).html());

		$.ajax({
					type:'POST',
					data:{iborrid:$("#ibid").val(),amoutval:$("#amountt").val()},
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
								get_sy(data);
							}
						}
					});
		$(".hb_list_box").hide();
}


function get_sy(data){
//$(".interest").html("预计收益：￥"+data.info).fadeIn();	
$("#yj_span").html(data.info+"元");
	if($("#hbje_span").html()!=""){
		var sf=Number($("#amountt").val())-Number($("#savehbje").val());
			sf=sf.toFixed(2);
		$("#sf_span").html(sf+" 元");
	}else{
		$("#sf_span").html($("#amountt").val()+" 元");
	}
        $(".interest_t").html("预计收益：￥"+data.info).fadeIn().next('b').show();
//      data.continue_reward='续投奖励：￥111';
        if(data.continue_reward!=''){
			$('.continue_reward').show().html(data.continue_reward);
			$(".invest-det-show-b .earnings p").css('lineHeight','25px');
			$('.invest-det-show-b .earnings .icon-question').css({'margin':'0','float':'none'});
		}else{
			$('.continue_reward').hide();
			$(".invest-det-show-b .earnings p").css('lineHeight','25px');
			$('.invest-det-show-b .earnings .icon-question').css('margin','0');
			}
		}															