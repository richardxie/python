/**
 *
//请求地址
var req_url = '/Invest/getIborrowTenderList';

//使用模板
var list_html_model = 'IborrowTenderFirstModel';

//使用不同的请求数据
var req_data_model = 'IborrowTenderFirstReqDate';

//生成的主体父级class名称
var html_box_show = '.html_box_show';

//生成的分页父级class名称
var page_box_show = '.page_box_show';

//进入页面自动加载
var auto_req_status = true;

下部引入js文件：src="/Public/JavaScript/Home/Invest/newborrow1.js"

*/

$(function(){
	/**
	 * eval方法调用不同模板
	 */
	function setModelHtml(pdata){
		var Quote = eval(list_html_model);
		return Quote(pdata);
	}
	/**
	 * eval方法调用不同请求数据
	 */
	function getReqModelDate(){
		var Quote = eval(req_data_model);
		return Quote();
	}
	/**
	 * 投资详情-》供应链金融-》投资列表》投资列表模板1
	 */
	function IborrowTenderSupplyChainModel(pdata){
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
             backhtml +='	<span class="gylxq_xmjl_time">'+item.addtime+'</span>';
             backhtml +='	<span class="gylxq_xmjl_name">'+item.username+'</span>';
             backhtml +='	<span class="gylxq_xmjl_money">￥'+item.account+'</span>';
             backhtml +='	<span class="gylxq_xmjl_icon '+classstype+'"></span>';
             backhtml +='</li>';  
		 });
		 return backhtml;
	}
	/**
	 * 投资详情-》资产金融-》投资列表》投资列表模板2
	 */
	function IborrowTenderAssetModel(pdata){
		 var backhtml='';
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
             backhtml +='	<span class="gylxq_xmjl_time">'+item.addtime+'</span>';
             backhtml +='	<span class="gylxq_xmjl_name">'+item.username+'</span>';
             backhtml +='	<span class="gylxq_xmjl_money">￥'+item.account+'</span>';
             backhtml +='	<span class="gylxq_xmjl_icon '+classstype+'"></span>';
             backhtml +='</li>';  
		 });
		 return backhtml;
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
	 * 已成功项目模板
	 */
	function IborrowSuccessModel(pdata){
		var backhtml = '';
		$.each(pdata, function(index, item) {
			backhtml += '<div class="invest-list-box gray">';
			backhtml += '<div class="invest-list-box1">';
			backhtml += '<div class="w1">';
			var name = item.name.length > 17 ? item.name.substr(0, 12) + "..." : item.name;
			backhtml += '<div class="invest-list2"><a href="/Invest/ViewBorrow/ibid/' + item.id + '" target="_blank" title="' + item.name + '">' + name + '</a>';
			backhtml += '</div>';
			backhtml += '</div>';
			backhtml += '<div class="w7 invest-show" data="0" pwd="' + item.invest_pwd_value + '">';
			backhtml += '<div class="w2">' + item.apr + '%</div>';
			//供应链奖励不再显示
//			if(item.gyl_zc_type == 'asset'){
//				backhtml += '<div class="w3">';
//				if (item.award_type == 2) {
//					backhtml += item.award_rate + '%';
//				} else if (item.award_type == 1) {
//					backhtml += '￥' + item.award_account;
//				} else {
//					backhtml += '无';
//				}
//				backhtml += '</div>';
//			}else{
//				backhtml += '<div class="w3">&nbsp;</div>';
//			}
			backhtml += '<div class="w3">&nbsp;</div>';
			
			backhtml += '<div class="w4">￥' + item.account + '</div>';
			if (item.repaystyle == '4') {
				backhtml += '<div class="w3 w20"><b>' + item.fatalism + '天</b></div>';
			} else {
				backhtml += '<div class="w3 w20">' + item.time_limit + '个月</div>';
			}
			backhtml += '<div class="w6">';
			backhtml += '<a class="invest-list4 invest-list10">' + item.status_msg + '</a>';
			backhtml += '</div>';
			backhtml += '</div>';
			backhtml += '</div>';
			backhtml += '</div>';
		});
		if (backhtml == '') {
			backhtml = '<div class="invest-list-box"><p  align="center">没有符合项目</p></div>';
		}
		return backhtml;
	}
	/**
	 * 已成功项目请求数据
	 */
	function IborrowSuccessReqDate(){
		// 传送的数据
		var obj = {};
		obj.goto_page = $('input[name=goto_page]').val();
		obj.page_href = $('input[name=page_href]').val();
		obj.from = $('input[name=from]').val();
		return obj;
	}
	
	
	/**
	 * 投资详情-》投资列表-》投资列表请求数据
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
	 * @uses 列表请求接口
	 * @author jhl
	 * @return json
	 */
	function getListDatas(){
		//获取请求数据
		var req_obj = getReqModelDate();
		//开始请求数据
		$.ajax({
			type:"POST",
			dataType:"json",
			url:req_url,
			data:req_obj,
			beforeSend:function(){
				 $(html_box_show).html('<div style="text-align:center;margin:60px 0px 0px 0px;"><img class="ajax_loader" src="/Public/Images/ajax-loader.gif" /></div>');
			},
			success:function(data){
				if(data.status > 0 && data.list.length > 0){
					 $(html_box_show).html(setModelHtml(data.list));
					 $(page_box_show).html(data.page);
				}else{
					$(html_box_show).html('');
					$(page_box_show).html('');
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
		var href = $(this).attr('href');
        if(href == ""){
            return false;
        }
    	$('input[name=page_href]').val(href);
        getListDatas();
        return false;
    });
    
	//跳转到指定页面事件
    $(document).on("click",".page_btn",function(){
        var goto_page = $(".goto_page").val();
        if(goto_page == ""){
            return false;
        }
        //清除page_href
        $('input[name=page_href]').val('');
        
        getListDatas();
    });
    
	//进入页面，加载项目
    if (typeof(auto_req_status) != "undefined" && auto_req_status == true) {
		$(document).ready(function(){
			getListDatas();
		});
    }
    
	//点击投资记录
	$(document).on('click','.iborrow_tender_record',function(){
		getListDatas();
	});
	
	//已成功列表供应链，资产金融切换
	$(document).on('click','.invest_gyl_button,.invest_zc_button',function(){
		var from = $(this).attr('data');
		$('input[name=from]').val(from);
		getListDatas();
	});
	
		//点击开心利是投资记录
	$(document).on('click', '.wfxq_tzjl_title', function() {
			//获取请求数据
			var req_obj = getReqModelDate();
			//开始请求数据
			$.ajax({
				type:"POST",
				dataType:"json",
				url:req_url,
				data:req_obj,
				beforeSend:function(){
					 $(html_box_show).html('<div style="text-align:center;margin:60px 0px 0px 0px;"><img class="ajax_loader" src="/Public/Images/ajax-loader.gif" /></div>');
				},
				success:function(data){
					if(data.status > 0 && data.list.length > 0){
						 $(html_box_show).html(setModelHtml(data.list));
						 $(page_box_show).html(data.page);
	 
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
						$(html_box_show).html('');
						$(page_box_show).html('');
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
});










