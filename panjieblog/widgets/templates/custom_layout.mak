<%namespace name="tw" module="tw2.core.mako_util"/>\
% for c in w.children_hidden:
    ${c.display() | n}
% endfor

% for i,c in enumerate(w.children_non_hidden):
	<div class="control-group ${(getattr(c, 'required', False) and ' required' or '') + (c.error_msg and ' error' or '')}">
        <label class="control-label">${c.label or ''}</label>
        <div class="controls">
            ${c.display() | n}
            <span id="${c.compound_id or ''}_error" class="help-inline">${c.error_msg or ''}</span>
        </div>
	</div>
% endfor
