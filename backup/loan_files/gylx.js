 $(function(){
 var $xm_li=$(".gylxq_box_title  li");
 $xm_li.click(function(){
	$(this).addClass("on")
	        .siblings().removeClass("on");
			var index=$xm_li.index(this);
			$(".gylxq_box_content>div") 
			              .eq(index).show()
						  .siblings().hide();
 });	
 })
 