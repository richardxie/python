window.vborrow = {
    borrow_type:0
};
//倒计时
function queue_timer(defSec,borrow_num,tnum) { 
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
		window.timeOut = window.setTimeout("queue_timer("+defSec+ ",'" + borrow_num + "','" + tnum + "')",1000);
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
            if(data.status==true){
                //window.RefalshTB(false);
                window.location.href = "/Invest/done";
            }else{
                if(data.data==0 && data.info){
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

var globalTimeout=null;
function showTime(tenderid, time_distance) { 
			  this.tenderid = tenderid; 
			//PHP时间是秒，JS时间是微秒 
			  this.time_distance = time_distance * 1000; 
			} 

$(document).ready(function(){	
		$(".left_check").not(":first").css("background-color","#ffffff");				   
		var modetype=1;
	 setTimeout(function(){RefalshList();},200);
	 setTimeout(function(){GetRank();},1000);
        var pagesize=20;	 
	
		var pageobj= new UI.Page({
	   		 toObj:$('#pagepanl'),
			 total:0,
			  size:pagesize,
			 star:1,
			 changepage:function(e1,e2,e3){
			   RefalshList();
		     }
		    });
		
		//获取排名
		function GetRank() {
			var state = $('#isopen').attr("data");
			if(state==1){
				$.ajax({
					type: "post",
					url: "/Invest/SearchRank",
					dataType: "json",
					beforeSend: function(XMLHttpRequest) {
					},
					success: function(context, textStatus) {
						if (context.status = 1) {
							if(context.data.length>20){
								var showdata = "当前"+context.data.substr(23);
							}else{
								var　showdata = '帐号余额不足';
							}
							
							$("#tdRankID").html(showdata);
						} else {
							$("#tdRankID").html("计算出错，您刷新试试！");
							//2.前后台通讯正常，但是后台逻辑发生错误，不能返回正确的数据
						}
					} 
				});
			}
		}
		 
		function RefalshList(){
			ViewList(modetype);
		}

		$('#RefalshList').click(function(e){
			RefalshList();
		} );

		function Vie(){
			  var selecttype=$('#selecttype').val();//融资类型 
			  var selectdate=$('#selectdate').val();//融资期限
			  var selectreplay=$('#selectreplay').val();//还款方式
			  var selectstate=$('#selectstate').val();//状态
			  var aprrange=$('#aprrange').attr("data");//年利率
			  var deadline=$('#deadline').attr("data");//融资期限
			  var account=$('#account').attr("data");//融资金额
                          var award=$('#award').attr("data");//融资金额
			  var myname=$.trim($('#myname').val());//融资者、融资标题
			  var selectname=$('#selectname').val();//融资者、融资标题

			  return  {'selecttype':selecttype,'selectdate':selectdate,'selectreplay':selectreplay,'selectstate':selectstate,'deadline':deadline,'aprrange':aprrange,'account':account,'award':award,'myname':myname,'selectname':selectname};
			  
		}
 
		function ViewList(pmode){
			var tpage={'page':1,'size':pagesize};
			if(pageobj){
				tpage=pageobj.GetParams();
			}
			//UI.loading('获取标列表','#uibPane');
			var dd=Vie();
			//$('#uibPane').html('<div style="text-align:center;"><img src="'+pubpath+'/Images/ajax-loader.gif" /></div>');
			$('#pagepanl').html('');
			$.ajax({
				type:'post',
				data:{'mode':pmode,'tpage':tpage,'sel':dd},
				url:GJsonUrl,
				beforeSend:function(){
					 $('#uibPane').html('<img class="ajax_loader" src="/Public/Images/ajax-loader.gif" />');
				},
				success:function(data){
					if(data.data.Total==0){
						
						$('#uibPane').html('<div style="width:200px;text-align:center; margin:0 auto; color:#9b9999">哦噢，当前没有相应项目</div>');
					}else{
						 if(data.status==1){ 
							isFinished=true;
							$('#uibPane').html(ViewBorrow(data.data.Rows));		            		
							pageobj.settotal(data.data.Total,tpage['page']); 			            	  	 
						}
					}
		            
		         }
			}); 
		 
		}
		function ViewBorrow(pdata){
			 var backhtml='';
			 $.each(pdata,function(index,item){
					backhtml+='<div class="new_list_box">';
						backhtml+='<div class="new_list_tit">';
							backhtml+=forborrowtypes(item.borrow_type);
							if(item.name.length>30){
								item.name=item.name.substr(0,20).toString();
								item.name=item.name+"...";
							}
							backhtml+='<span tag="'+ Borrowpath + item.id +'" class="new_bname">'+item.name+'</span>';
							backhtml+='<span class="new_btime">';
                                                        if(item.repaystyle=='4'){
                                                                backhtml+='<div class="w3">'+item.fatalism+'天</div>';
                                                        }else{
                                                                backhtml+='<div class="w3">'+item.time_limit+'个月</div>';
                                                        }                           
                                                        backhtml+='</span>';
						backhtml+='</div>';
						backhtml+='<div class="new_list_body">';
							backhtml+='<div class="new_list_head"><img src="' + Userimgpath + item.user_id + '/middle.jpg"  onerror="finddefuserimg($(this));" /></div>';
							backhtml+='<div class="new_list_midbox">';
								backhtml+='<div class="new_midbox_1">';
									if(UI.isempty(item.pic)){
                                        backhtml+='<img  src="'+pubpath+'"/Images/credit/rank_1.gif" />';
                                }else{
                                        backhtml+='<img  src="'+pubpath+'/Images/'+ item.pic+'" />';
                                }
									if(item.username.length>10){
										item.username=item.username.substr(0,10)+"...";
									}
									backhtml+='<span class="user_name">'+item.username+'</span>';
								backhtml+='</div>';
								backhtml+='<div class="new_midbox_2">';
									backhtml+='<div class="w6">';
										backhtml+='<span id="bar_'+item.id+'">';
											backhtml+=forborrowstatus(item.status,item.destine_type,item.destine_time,item.bar);
										backhtml+='</span>';
									backhtml+='</div>';
								backhtml+='</div>';
								backhtml+='<div class="new_midbox_3">' + item.remain + '/'+ item.account +'</div>';
							backhtml+='</div>';
							backhtml+='<div class="new_list_right">';
								backhtml+='<div class="new_rightbox_1">';
                                                                        if(item.award_type !=0){
                                                                                backhtml+='<div class="new_right_lv">';
                                                                                if(item.award_type==2){                                                                        
                                                                                        backhtml+='+'+item.award_rate +'%';
                                                                                }else if(item.award_type==1){                                                      
                                                                                        backhtml+='￥'+item.award_account;
                                                                                }
                                                                                backhtml+='</div>';
                                                                        }
									backhtml+='<div class="new_right_suo">';
                                                                        if(UI.isempty(item.borrowpwd) && item.status==1 && item.destine_type!=1){
                                                                                backhtml+='<b class="icon-img invest-list5 invest-show-line" data="0" pwd=""></b>';
                                                                        }else if(item.borrowpwd){
                                                                                backhtml += '<b title="此标为密码标" class="icon-20 icon-20-lock"></b>';
                                                                        }
                                                                        backhtml+='</div>';
								backhtml+='</div>';
								backhtml+='<div class="new_rightbox_2">'+item.apr+'%</div>';
							backhtml+='</div>';
						backhtml+='</div>';
					  backhtml+='</div>';
			 });
			 return backhtml;
		}
			
			 $(document).on("click",".new_list_box",function(e){
				  e.stopPropagation();
					window.open($(this).find(".new_bname").attr("tag"));
				});
				

		
    function forborrowstatus(pstatus,destine_type,destine_time,bar){
        backhtml="";
        switch (pstatus) {
            case "1":
                if(destine_type==1){
                    backhtml += '<a class="invest-list4 invest-list9">'+showunixtimeV(destine_time,'dateandtime')+'开始</a>';
                }else{
                    if(bar>=80){
                        backhtml+='<div class="progress red"><a><b style="width:'+subnumber(bar,2)+'%"></b></a></div>';
                    }else{
                        backhtml+='<div class="progress"><a><b style="width:'+subnumber(bar,2)+'%"></b></a></div>';
                    }
                }
                break;
            case "7":
                backhtml+='<a class="invest-list4 invest-list10" >还款中</a>'; 
                break;
            case "8":
                backhtml+='<a class="invest-list4 invest-list8" >已还清</a>'; 
                break;
            case "9":
                backhtml+='<a class="invest-list4 invest-list8" >逾期的标</a>'; 
                break;		 	 
            default:
                backhtml+='未知';
        }
         
        return backhtml;
    }
    function forborrowmode(bmode){
        backhtml="";
        switch (bmode) {
            case "0":
                backhtml+="按月分期"; 
                break;
            case "3":
                backhtml+="到期还本"; 
                break;
            case "4":
                backhtml+="按天到期"; 
                break;	
            case "5":
                backhtml+="到期全还"; 
                break;	 
            default:
                backhtml+="立即还款";
        }
        return backhtml;
    }
    function forborrowuser(puse){
        backhtml="";
        switch (puse) {
            case '6':
                backhtml+="净值周转";
                break;
            case '7':
                backhtml+="股东融资";
                break; 
            case '10':
                backhtml+="装修";
                break; 
            case '11':
                backhtml+="旅游";
                break; 
            case '12':
                backhtml+="购车";
                break; 
            case '13':
                backhtml+="家电";
                break; 
            case '14':
                backhtml+="其他";
                break; 	 
            case '15':
                backhtml+="结婚";
                break; 
            case '2':
                backhtml+="短期周转";
                break;
            case '3':
                backhtml+="实业周转";
                break;	
            case '4':
                backhtml+="购买生产材料";
                break;	
            case '5':
                backhtml+="快乐秒还";
                break;		
            case '9':
                backhtml+="黄花梨";
                break;		 
            default:
                backhtml+="站内周转";
        }
        return backhtml;
    }
    function forborrowtype(borrowpwd,ptype,repaystyle){
        backhtml="";
        switch (ptype) {
            case '1':
                backhtml+='<b title="此标为企业融资" class="icon-img icon-20 icon-20-qy"></b>';
                break;
            case '2':
                backhtml+='<b title="此标为信用融资" class="icon-img icon-20 icon-20-xy"></b>';
                break;
            case '3':
                backhtml+='<b title="此标为抵押融资" class="icon-img icon-20 icon-20-dy"></b>';
                break;
            case '4':
                backhtml+='<b title="此标为担保融资" class="icon-img icon-20 icon-20-db"></b>';
                break;
            case '5':
                backhtml+='<b title="快乐秒还，满标后立刻回款，待收大于5千的用户可投" class="icon-img icon-20 icon-20-mb"></b>';
                 break;
            case '6':
                backhtml+='<b title="此标为净值融资" class="icon-img icon-20 icon-20-jz"></b>';
                break;
            case '7':
                backhtml+='<b title="此标为股东融资" class="icon-img icon-20 icon-20-gd"></b>';
                break;
            case '9':
                backhtml+='<b title="此标为创业融资" class="icon-img icon-20 icon-20-cy"></b>';
                break;
            case '11':
                backhtml+='<b title="此标为工薪融资" class="icon-img icon-20 icon-20-gx"></b>';
                break;
            default:
            backhtml+="未知";
        }

			if(!UI.isempty(borrowpwd)){
				backhtml = '<b title="此标为密码标" class="icon-img icon-20 icon-20-lock"></b>';
			}
			return backhtml;
		} 
		
		function forborrowtypes(ptype){
			backhtml="";
			switch (ptype) {
				case '1':
                                        backhtml+='<img title="此标为企业融资" src="'+pubpath+'/Images/newinvest/icon/icon-qy.png" />';
			 		break;
			 	case '2':
                                        backhtml+='<img title="此标为信用融资" src="'+pubpath+'/Images/newinvest/icon/icon-xy.png" />';
			 		break;
			 	case '3':
                                        backhtml+='<img title="此标为抵押融资" src="'+pubpath+'/Images/newinvest/icon/icon-dy.png" />';
			 		break;
			 	case '4':
                                        backhtml+='<img title="此标为担保融资" src="'+pubpath+'/Images/newinvest/icon/icon-db.png" />';
			 		break;
			 	case '5':
                                        backhtml+='<img title="此标为秒还融资" src="'+pubpath+'/Images/newinvest/icon/icon-mh.png" />';
			 		 break;
			 	case '6':
                                        backhtml+='<img title="此标为净值融资" src="'+pubpath+'/Images/newinvest/icon/icon-jz.png" />';
			 		break;
			 	case '7':
                                        backhtml+='<img title="此标为股东融资" src="'+pubpath+'/Images/newinvest/icon/icon-gd.png" />';
			 		break;
			 	case '9':
                                        backhtml+='<img title="此标为创业融资" src="'+pubpath+'/Images/newinvest/icon/icon-cy.png" />';
			 		break;
			 	case '11':
                                        backhtml+='<img title="此标为工薪融资" src="'+pubpath+'/Images/newinvest/icon/icon-gx.png" />';
			 		break;
			 	default:
		 		backhtml+="未知";
			}

			return backhtml;
		}
		
		function showunixtimeV(punixtime,type){
                    var farmatStr = "yyyyMMdd hh:mm";
                    if(type == 'date'){
                        farmatStr = "yyyyMMdd";
                    }else if(type == 'dateandtime'){
                        farmatStr = "MM月dd日 hh:mm";
                    }else if(type == 'dateandtime2'){
                        farmatStr = "yyyy-MM-dd hh:mm";
                    }
			var unixTimestamp = new Date(punixtime* 1000); 
			commonTime = unixTimestamp.Format(farmatStr);
			//document.write(commonTime);
			 return commonTime;
		}
		
		Date.prototype.Format = function(fmt)   
		{ //author: meizz   
		  var o = {   
		    "M+" : this.getMonth()+1,                 //月份   
		    "d+" : this.getDate(),                    //日   
		    "h+" : this.getHours(),                   //小时   
		    "m+" : this.getMinutes(),                 //分   
		    "s+" : this.getSeconds(),                 //秒   
		    "q+" : Math.floor((this.getMonth()+3)/3), //季度   
		    "S"  : this.getMilliseconds()             //毫秒   
		  };   
		  if(/(y+)/.test(fmt))   
		    fmt=fmt.replace(RegExp.$1, (this.getFullYear()+"").substr(4 - RegExp.$1.length));   
		  for(var k in o)   
		    if(new RegExp("("+ k +")").test(fmt))   
		  fmt = fmt.replace(RegExp.$1, (RegExp.$1.length==1) ? (o[k]) : (("00"+ o[k]).substr((""+ o[k]).length)));   
		  return fmt;   
		} ;
		
		showTime.prototype.setTimeShow = function () { 
				var timer = $("#lefttime_" + this.tenderid); 
				var str_time; 
				var int_day, int_hour, int_minute, int_second; 
				time_distance = this.time_distance; 
				this.time_distance = this.time_distance - 1000; 
				if (this.time_distance > 0) { 
					int_day = Math.floor(time_distance / 86400000); 
					time_distance -= int_day * 86400000; 
					int_hour = Math.floor(time_distance / 3600000); 
					time_distance -= int_hour * 3600000; 
					int_minute = Math.floor(time_distance / 60000); 
					time_distance -= int_minute * 60000; 
					int_second = Math.floor(time_distance / 1000); 
					if (int_hour < 10) 
					int_hour = "0" + int_hour; 
					if (int_minute < 10) 
					int_minute = "0" + int_minute; 
					if (int_second < 10) 
					int_second = "0" + int_second; 
					str_time = int_day + "天" + int_hour + "时" + int_minute + "分" + int_second + "秒"; 
					timer.text(str_time); 
					var self = this; 
					setTimeout(function () { self.setTimeShow(); }, 1000); //D:正确 
				} else { 
					timer.text("标已经过时"); 
					return; 
				} 
			};
		 
			
		  
			function subnumber(num){
					var num=new Number(num);
					var pos=num.toString().indexOf(".");
					if(pos>0){
						return num.toString().substr(0,pos+3);
					}else{
							return num.toString();
					 }
			}

		   
		   $('.leftnav_tit2').click(function(){ 
		    
		
			   $('#selectname').val('0');
			   $(this).addClass('tit2click');
			   $(this).siblings().removeClass('tit2click');
			   
			   var tag = $(this).attr("tag");
			   var data = $(this).attr("data");
			   $('#'+tag).val(data);
			 
			   pageobj.currpage(1); 
			   
			   if (globalTimeout != null) {
    clearTimeout(globalTimeout);
  }
  globalTimeout = setTimeout(function() {
    globalTimeout = null;   
 				 	  ViewList(1);	 

  }, 1000); 
				 
				 
			 
			
				 
		   });
		   
		   $('.invest-option7').click(function(){
			   $('.invest-option8').slideUp(150);
			   $('.invest-option6').show();
		   });
		   
		   $('.invest-option6').click(function(){
			   $(this).hide();
			   $('.invest-option8').slideDown(150);
		   });
		   		   
		   $('.invest-show').live("click",function(){
			   var pwd = $(this).attr('pwd');
			   if(!UI.isempty(pwd)){
				   return;
			   }
			   var data = $(this).attr("data");
			   $(".invest-list-box").removeClass("active");
			   $(".invest-list-box").find('.invest-show').attr("data",0);
			   $(".invest-list-box").find('.invest-show-line').removeClass('invest-list5a');
			   $(".invest-list-box").find('.invest-show-line').removeClass('invest-list5');
			   $(".invest-list-box").find('.invest-show-line').addClass('invest-list5');
			   $(".invest-list-det7").hide();
			   $(".amoutval").val('');
			   if(data==0){
				   $(this).attr("data",1);
				   $(this).parents(".invest-list-box").addClass("active");
				   $(this).find('.invest-show-line').removeClass('invest-list5');
				   $(this).find('.invest-show-line').addClass('invest-list5a');
			   }else{
				   $(this).attr("data",0);
				   $(this).parents(".invest-list-box").removeClass("active");
				   $(this).find('.invest-show-line').removeClass('invest-list5a');
				   $(this).find('.invest-show-line').addClass('invest-list5');
			   }
		   });
		   
		   $('#searchborrow').click(function(){
			   $('#selectname').val('1');
			   $(".isselect").removeClass('active');
			   $(".firstselect").addClass('active');
			   $("#selecttype").val(0);
			   $("#selectdate").val(0);
			   $("#selectreplay").val(0);
			   $("#selectstate").val(0);
			   $("#closesearch").show();
			   ViewList(modetype);
		   });
		   
		   $('#closesearch').click(function(){
			   location.reload();
		   });
		   
		   $('.showamount').live("click",function(){ 
			   var inacount = 0;
			   var iborrid = $(this).attr("iborrid");
			   var zhye = parseInt($('#usermoney').val());
			   var hxjk = $(this).attr("maycase");
			   var zdtbe= parseInt($(this).attr("ibowbig"));
                           hxjk=hxjk.replace(/\,/ig,'');//去掉千分号
			   if(isNaN(zdtbe)){zdtbe=hxjk+100;}  
			   	if(isNaN(zhye)){
			   		inacount = 0;
			   	}else if(hxjk>=zhye&&zhye<zdtbe){
					inacount = zhye;
				}else if(hxjk>=zhye&&zhye>zdtbe){
					inacount = zdtbe;
				}else if(hxjk<zhye&&hxjk<zdtbe){
					inacount = hxjk;
				}else if(hxjk<zhye&&hxjk>zdtbe){
					inacount = zdtbe;
				} 
			   	$(this).siblings('.amoutval').val(inacount);
			   	var obj = $(this).parent().siblings('.invest-list-det7');
			   	obj.show();
			   	$.ajax({
					type:'post',
					data:{'iborrid':iborrid,'amoutval':inacount},
					url:Incomeinfo,
					success:function(data){
			            if(data.status==1) { 
			            	obj.children(".hopeincome").html(data.info);
                                        if(data.continue_reward!=''){
                                            $('.continue_reward').html(data.continue_reward).show();
                                        }else{
                                            $('.continue_reward').hide();
                                        }
		                }
			         }
				});
			   	
		   });
		   

		   $('.amoutval').live("blur",function(){ 
			   var inacount = $(this).val();
			   var obj = $(this).parent().siblings('.invest-list-det7');
			   if(inacount==''){
				   obj.hide();
				   return;
			   }
			   var iborrid = $(this).attr("iborrid"); 	
			   	obj.show();
			   	$.ajax({
					type:'post',
					data:{'iborrid':iborrid,'amoutval':inacount},
					url:Incomeinfo,
					success:function(data){
			            if(data.status==1) { 
			            	obj.children(".hopeincome").html(data.info);
                                        if(data.continue_reward!=''){
                                            $('.continue_reward').show().html(data.continue_reward);
                                        }else{
                                            $('.continue_reward').hide();
                                        }
		                }else{
		                	obj.children(".hopeincome").html('<font style="color:red">&nbsp;&nbsp;&nbsp;&nbsp;'+data.info+'</font>');
		                }
			         }
				});
			   	
		   });
		   
		   $('#aprrange').click(function(){
			   var data = $(this).attr("data");
			   $(this).attr("data",getupdownnumber(data,$(this)));
			   $('#deadline').attr("data","0");
			   $('#deadline').find("b").attr("class","normal");
			   $('#account').attr("data","0");
			   $('#account').find("b").attr("class","normal");
                           $('#award').attr("data","0").find("b").attr("class","normal");
			   ViewList(modetype);
		   });
		   
		   $('#deadline').click(function(){
			   var data = $(this).attr("data");
			   $(this).attr("data",getupdownnumber(data,$(this)));
			   $('#aprrange').attr("data","0");
			   $('#aprrange').find("b").attr("class","normal");
			   $('#account').attr("data","0");
			   $('#account').find("b").attr("class","normal");
                           $('#award').attr("data","0").find("b").attr("class","normal");
			   ViewList(modetype);
		   });
		   
		   $('#account').click(function(){
			   var data = $(this).attr("data");
			   $(this).attr("data",getupdownnumber(data,$(this)));
			   $('#aprrange').attr("data","0");
			   $('#aprrange').find("b").attr("class","normal");
			   $('#deadline').attr("data","0");
			   $('#deadline').find("b").attr("class","normal");
                           $('#award').attr("data","0").find("b").attr("class","normal");
			   ViewList(modetype);
		   });
		   $('#award').click(function(){
			   var data = $(this).attr("data");
			   $(this).attr("data",getupdownnumber(data,$(this)));
			   $('#aprrange').attr("data","0").find("b").attr("class","normal");
			   $('#deadline').attr("data","0").find("b").attr("class","normal");
                           $('#account').attr("data","0").find("b").attr("class","normal");
			   ViewList(modetype);
		   });
		   
		   
		   function getupdownnumber(data,obj){
			   switch (data) {
			 	case '0':
			 		$(obj).find("b").attr("class","down img1");
			 		data = 1;
				 break;
			 	case '1':
			 		$(obj).find("b").attr("class","up img1");
			 		data = 2;
				 break; 
			 	case '2':
			 		$(obj).find("b").attr("class","normal");
			 		data = 0;
				 break;
			 	default:
			 		$(obj).find("b").attr("class","normal");
			 		data = 0;
			 	break;
			   }
			   return data;
		   }
		   
		   $("#cancel2,#cinvest").click(function() {
				$('#coninvest').hide();
				$("#incheck").removeAttr("disabled");
				$("#input2").val('');
				$("#uiviewmsg").html('点击按钮表示您同意支付投资金额');
				$("#suretender").val('确认投标'); 
				$("#suretender").removeAttr("disabled");
				showHiheInput();
			})
			//投标 按钮 
			$(".incheck").live("click",function() { 
        var _this = this;
        window["vborrow"].borrow_type = $(_this).siblings(".borrow_type_inp").val();
				$("#showinfo").html("");
				var amoutval = $.trim($(this).siblings('.amoutval').val());
				var obj = $(this).parent().siblings('.invest-list-det7');
				obj.show();
				if (!amoutval || amoutval.replace(/^[1-9][0-9].*$|^(0|[1-9]+)\.\d{0,2}$/g, '')) {
					obj.children(".hopeincome").html('<font style="color:red">&nbsp;&nbsp;&nbsp;金额不是有效数字</font>');
					return false;
				}
				
				if(amoutval<50){
					obj.children(".hopeincome").html('<font style="color:red">&nbsp;&nbsp;&nbsp;投资金额必须大于50</font>');
					return false;
				}
				
				
				var ibid = $(this).attr("iborrid"); 
				$.ajax({
					dataType: "json", 
					url: CurrPath + '/investcheck/ibid/' + ibid,
					dataType:"json",
					success: function(data) {
						if(data.status==503){
							location.href = '/NewLogin';
						}else{
							if(data.status==129){
								$.ajax({
									type:'post',
									data:{'iborrid':ibid,'amoutval':amoutval},
									url:GetBorrowinfo,
									dataType:"json",
									success:function(data){  
							            if(data.status) {   
							            	$("#biaoimg").html(forborrowtypes(data.info.borrow_type));  
											$("#balance").html(subnumber(data.info.useMoney,2)); 
											$("#yearapr").html(data.info.apr+"%"); 
											if(data.info.award_rate>0){
							            		$("#awardrate").html("+"+data.info.award_rate+"%");
							            	}
							            	if(data.info.repaystyle=='4'){
							            		$("#timelimit").html(data.info.fatalism+"天");
											 }else{
												 $("#timelimit").html(data.info.time_limit+"个月");
											 }
							            	$("#input1").val(data.info.amoutval);
							            	$("#input2").val(data.info.amoutval);
							            	$("#repaystyle").html(forborrowmode(data.info.repaystyle));
							            	$("#incoming").html(data.info.income);
							            	$("#nowmaycase").val(subnumber(data.info.remain,2));
							            	$("#nowibowbig").val(data.info.most_account);
							            	$("#nowiborrid").val(data.info.id);
							            	$("#nowiborrnum").val(data.info.borrow_num);
							            	
							            	$("#coninvest").show();
                                                                        popcenterWindow('#coninvest #animate');//弹窗居中
							            	$("#password").focus();
						                }
							         }
								});
							
							}else{
								//showCantendErr(data.status);
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
		   
		   $(".refalsh").live("click",function(){
			   var ibid = $(this).attr("iborrid");
			   var obj = $(this);
			   obj.siblings().html('');	
			   $.ajax({
					type:'post',
					data:{'iborrid':ibid},
					url:GetBorrowinfoOne,
					success:function(data){
			            if(data.status==1) { 
			            	obj.parents().parents().siblings(".invest-list-det5").children(".invest-list-det6").children(".showamount").attr("maycase",subnumber(data.info.remain,2));
			            	obj.siblings().html('￥'+subnumber(data.info.remain,2));		            	
			            	var backhtml = forborrowstatus(data.info.status,data.info.destine_type,data.info.destine_time,data.info.bar);
			            	$("#bar_"+ibid).html(backhtml);
			            	if(data.info.status!=1){
			            		$("#bt_"+ibid).attr("disabled","disabled");
			            	}
		                }
			         }
				});
		   });
		   
		   function showCantendErr(errnum) {
				switch (errnum) {
				case 503:
					ShowMsgdiv("检查是否登录", "您还没有的登录，不能进行投标！", "去网站登录吧 →", Loginurl);
					break;
				case 122:
					ShowMsgdiv("检查认证", "您还有未进行认证的项目，不能进行投标！", "去安全中心完善你的认证 →", Tosaft);
					break;
				case 123:
					ShowMsgdiv("检查交易密码", "您交易密码未设置，不能进行投标！", "去安全中心设置 →", Tosaft);
					break;
				case 125:
					ShowMsgdiv("检查账户余额", "账户余额为空，不能进行投标！", "去充值吧 →", "/Account/FundsManagement/title/Recharge");
					break;
				case 125:
					ShowMsgdiv("检查账户余额", "账户余额不足，不能进行投标！", "去充值吧 →", "/Account/FundsManagement/title/Recharge");
					break;
				case 108:
					ShowMsgdiv("检查是否是自己所发标", "此标是自己所发，不能进行投自己所发标！", "请选择其它标 →", "/Invest/index");
					break;
				case 127:
					ShowMsgdiv("检查标密码", "标密码错误，不能进行投标！", "", "#");
					break;
				case 126:
					ShowMsgdiv("错误", "标无效", "请联系我们");
					break;
				default:
					ShowMsgdiv("错误", "未知错误", "请联系我们");
		
				}
			}
			
			function ShowMsgdiv(ptitle, pmsg, purltext, purl) {

				$("#eee").html(ptitle);
				$("#wcon b").html(pmsg + "<br/>");
				$("#wcon span").addClass('orange acc-id24');
				$("#wcon a").addClass('link01');
				//$("#wcon span").append("1111");
				$("#wcon a").html(purltext);
				$("#wcon a").attr("href", purl);
				$('#aaa').show();
			}
			$("#closew").click(function() {
				$('#aaa').hide();
			});
			
			
			$("#showmoney").click(function(){
				$(this).hide();
				$("#inputmomey").show();
				$("#input2").focus();
			});
			
			$("#biggestmoney").click(function(){
				var inacount = 0;
				var iborrid = $("#nowiborrid").val();
				var zhye = parseInt($("#usermoney").val());
				var hxjk = $("#nowmaycase").val();
				var zdtbe= parseInt($("#nowibowbig").val());
				if(isNaN(zdtbe)){zdtbe=parseInt(hxjk)+100;}  
				if(isNaN(zhye)){
				   inacount = 0;
				}else if(hxjk>=zhye&&zhye<zdtbe){
					inacount = zhye;
				 }else if(hxjk>=zhye&&zhye>zdtbe){
					inacount = zdtbe;
				 }else if(hxjk<zhye&&hxjk<zdtbe){
					inacount = hxjk;
				 }else if(hxjk<zhye&&hxjk>zdtbe){
					inacount = zdtbe;
				 } 


        $("#input2").val(inacount);

    });
        
    $("#suremoney").click(function(){
        var iborrid = $("#nowiborrid").val();
        var amoutval = $("#input2").val();
        if (!amoutval || amoutval.replace(/^[1-9][0-9].*$|^(0|[1-9]+)\.\d{0,2}$/g, '')) {
            $("#uiviewmsg").html('<font style="color:red;">投资金额不是有效数字</font>');
            $("#input2").focus();
            return false;
        }
        
        if(amoutval<50){
            $("#uiviewmsg").html('<font style="color:red;">投资金额必须大于50</font>');
            $("#input2").focus();
            return false;
        }
        
        $.ajax({
            type:'post',
            data:{'iborrid':iborrid,'amoutval':amoutval},
            url:Incomeinfo,
            success:function(data){
                if(data.status==1) { 
                    $("#incoming").html(data.info);
                    $("#input1").val(amoutval);
                    showHiheInput();
                            if(data.continue_reward!=''){
                                $('.continue_reward').html(data.continue_reward).show();
                            }else{
                                $('.continue_reward').hide();
                            }
                }
             }
        });
    });
    
    $("#refreshmomey").click(function(){
        $("#balance").html('');
        $.ajax({
            "type": "POST",
            "dataType": 'json',
            url: "/Invest/getAccountInfo",
            success: function(data) {
                if (data.status == 1) {
                    $("#balance").html(data.formated_money);
                }
            }
        })
    });
    
    $("#password").focus(function(){
        showHiheInput();
    });
    
    $("#animate").bind('click',showHiheInput);	
    $("#showmoney,#biggestmoney,#input2").bind('click',stopBubble);
    
    function showHiheInput(){
        $("#showmoney").show();
        $("#inputmomey").hide();
    }
    
    //阻止事件冒泡函数
    function stopBubble(e){  
        if (e && e.stopPropagation)  
            e.stopPropagation()  
        else  
            window.event.cancelBubble=true  
    }
    
    //检测交易密码和投标
    $("#suretender").bind('click',subtender);
    $("#password").bind('keydown',function(event){var e = event || window.event;if(!e.ctrlKey && e.keyCode ==13){subtender()}});
    
    function subtender(){
        if ($("#suretender").val() == '正在投标..') {
            return;
        }			
        var ibid = $('#nowiborrid').val();
        var ppay = $.trim($("#password").val());
        var iborrownumid = $("#nowiborrnum").val();
        var amountt = $("#input1").val();
        if (ppay == "") {
            $("#uiviewmsg").html('<font style="color:red;">交易密码不能为空</font>');
            $("#password").focus();
            return;
        } else {
            $("#suretender").val('正在投标..');

            $.ajax({
                type: 'POST',
                url: '/Invest/checkppay',
                data: {
                    p_pay: ppay,
                    ibnum: iborrownumid,
                    amount: amountt,
                     '__hash__':$("input:hidden[name=__hash__]").val()
                },
                cache: false,
                success: function(data) {
                    if (data.status == 119) {
                        //if(window["vborrow"].borrow_type == 5){
                            //$.idialog.show({icon:   "loading" , msg: data.info, location: '/Invest/done'}); 
                            $(".queue-box").fadeIn(600);
                            var tnum = data.tnum;
                            //var borrow_num = $("#iborrownumid").val();
                            queue_timer(16, iborrownumid, tnum);
                       /* }else{
                            $.idialog.show({icon:   "loading" , msg: data.info, location: '/Invest/done'}); 
                        }*/
                        
                    } else if (data.status == 118) {
                        $("#uiviewmsg").html('<font style="color:red;">失败，' + data.info+'</font>');
                        $("#suretender").val('重投'); 
                    } else if (data.status == 117) {
                        $('.invest_mb').removeClass('none');
                    } else if (data.status == 101||data.status==102) {
                        $('#suretender').val('确认投标')
                         $('#ppay_error').removeClass('none').find('span').html(data.info)
                    }else if(data.status==200){
                        $("#showinfo").html(data.info);
                         var timer=	window.setInterval(function(){
                        $.get("/Invest/getTenderMsg/",{'msgid':data.msgid},function(d){
                                if(d.status==119){
                                        RefalshTB(false);
                                         window.location.href="/Invest/done";
                                    }else{
                                        $("#showinfo").html(d.info);
                                        clearInterval(timer);
                                    }
                            }) 
                    }, 1000);  
                    }else if(data.status==203){
                        $("#showinfo").html(data.info);
                        $('#suretender').val('重投'); 
                    }else { 
                        $("#uiviewmsg").html('<font style="color:red;">失败，' + data.info+'</font>');
                        $("#suretender").val('重投'); 
                         
                    }
                },
                error: function(xhr, status, text) {
                    $("#uiviewmsg").html('<font style="color:red;">'+text+'</font>');
                    $("#button").val('重投');
                }
            });
        }
    }
		
		$('.invest-list-box').live("hover",function(){
			var pwd = $(this).attr('pwd');
			if(UI.isempty(pwd)){
				$(this).children(".invest-list-box1").children(".w6").children(".invest-show").hide();
			}
		});

		 $('.isselect').click(function(){ 
		    
		
			   $('#selectname').val('0');
			   $(this).addClass('active');
			   $(this).siblings().removeClass('active');
			   
			   var tag = $(this).attr("tag");
			   var data = $(this).attr("data");
			   $('#'+tag).val(data);
			 
			   pageobj.currpage(1); 
			   
			   if (globalTimeout != null) {
    clearTimeout(globalTimeout);
  }
	  globalTimeout = setTimeout(function() {
	    globalTimeout = null;   
	 				 	  ViewList(1);	 

	  }, 1000);	
    });
		 
});