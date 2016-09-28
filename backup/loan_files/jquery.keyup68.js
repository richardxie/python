/*
 * author: tcdona
 * data: 2012/08/15
 * version: 0.1
 * location: E:\project\设计部\中国特产网v1.0html\js\jquery.keyup68.js
 *
 *
 */

(function($) {
	$.fn.keyup68 = function(/* selector */) {
		// var opts = $.extend({}, $.fn.keyup68.defaults, {nextSelector: selector});
		
		return this.each(function() {
			var root = $(this)
			  , focusable
			  , next
			  ;
			
			root
			.on('keydown', 'input, textarea, select', function(e) {
				if (13 === e.keyCode) {
					focusable = root.find('[keyup68-next=true]');
					next = focusable.eq( focusable.index(this) + 1 );
					if (next.length) {
						next.focus();
					} else {
						if (this.tagName == "TEXTAREA") {
							return true;
						}
						root.submit();
						return true;
					}
					return false;
				}
			})
			.on('keydown', '[keyup68-number=true]', function(e) {
				var code = e.keyCode;
				if (
					// 数字
					(code >= 48 && code <= 57) || (code >= 96 && code <= 105)
					// 删除
					|| code == 8 || code == 46
					// home end
					|| code == 36 || code == 35
					// shift ctrl
					|| code == 16 || code == 17
					// tab
					|| code == 9
					// 左右移动
					|| code == 37|| code == 39
				) {
					return true;
				} else {
					return false;
				}
			})
			.on('keydown', '[keyup68-float=true]', function(e) {
				var code = e.keyCode;
				if (
					// 数字
					(code >= 48 && code <= 57) || (code >= 96 && code <= 105)
					// 删除
					|| code == 8 || code == 46
					// home end
					|| code == 36 || code == 35
					// shift ctrl
					|| code == 16 || code == 17
					// tab
					|| code == 9
					// 左右移动
					|| code == 37|| code == 39
					// 小数点
					|| code == 110 || code == 190
				) {
					if (
						(code == 110 || code == 190)
						// 只有一个 小数点
						&& $(this).val().indexOf(".") >= 0
					) {
						e.keyCode = 0;
						return false;
					}
					return true;
				} else {
					return false;
				}
			})
			;
		});
	};
	$.fn.keyup68.defaults = {
		// 由于只有一个配置项/参数 所以是直接提供 参数: 下一个(焦点元素的) class 选择器就可以了
		// nextSelector: 'input, textarea, select'
		// 2012 08 27 取消了所有的(唯一的)配置参数 改成了用自定义属性 keyup68-next="true" keyup68-number="true" 来判断 解决 keyup68 同 formValidator 的兼容问题
		// formValidator 会把 input 元素的 class 重新设值! [bug!]
	};
})(jQuery);