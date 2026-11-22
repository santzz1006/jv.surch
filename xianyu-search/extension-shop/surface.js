'use strict';
// The action popup needs an intrinsic width before Chrome measures its document.
// Only the embedded panel should derive its width from a parent viewport.
document.documentElement.dataset.surface = window.top === window ? 'action' : 'embedded';
chrome.runtime.sendMessage({type:'gb-ensure-overlay'}).catch(()=>{});
