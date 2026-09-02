// Usage: node cdp-upload-multi.mjs <wsUrl> <inputIndex> <file1> [file2...]
const [ws, idxStr, ...files] = process.argv.slice(2);
const idx = parseInt(idxStr,10);
const sock = new WebSocket(ws);
let id=0; const pend={};
function send(method,params,sessionId){return new Promise((res,rej)=>{const i=++id; pend[i]={res,rej}; sock.send(JSON.stringify({id:i,method,params,sessionId}))})}
sock.onmessage=(ev)=>{const m=JSON.parse(ev.data); if(m.id&&pend[m.id]){m.error?pend[m.id].rej(new Error(JSON.stringify(m.error))):pend[m.id].res(m.result); delete pend[m.id]}};
sock.onopen=async()=>{
 try{
  const doc=await send('DOM.getDocument',{depth:-1,pierce:true});
  const q=await send('DOM.querySelectorAll',{nodeId:doc.root.nodeId,selector:'input[type=file]'});
  if(!q.nodeIds||q.nodeIds.length<=idx) throw new Error('input index out of range, found '+(q.nodeIds||[]).length);
  await send('DOM.setFileInputFiles',{files, nodeId:q.nodeIds[idx]});
  // fire input+change for Angular
  const rn=await send('DOM.resolveNode',{nodeId:q.nodeIds[idx]});
  await send('Runtime.callFunctionOn',{objectId:rn.object.objectId, functionDeclaration:'function(){this.dispatchEvent(new Event("change",{bubbles:true}));}'});
  console.log('OK set', files.length, 'files on input', idx);
  process.exit(0);
 }catch(e){console.error('FAIL', e.message); process.exit(1)}
};
sock.onerror=(e)=>{console.error('WS error'); process.exit(1)};
