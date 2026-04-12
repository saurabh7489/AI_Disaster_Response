const ACTION_NAMES=["Ambulance Dispatch","Food Supply","Rescue Boat","Wait / Monitor","Deploy Doctors","Setup Medical Camp","Water Supply","Distribute Medicines","Helicopter Rescue","Evacuation Bus","Quarantine Zone","Sanitize Area","Distribute Masks","Vaccination Drive","Alert Authorities","Monitor Situation","Restore Electricity","Setup Comms Network","Temporary Shelter","Clear Road Blockages"];
let totalScore=0,autoRunInterval=null;
function boolBadge(v){return v?'<span class="bool-yes">Yes</span>':'<span class="bool-no">No</span>'}
function priorityBadge(p){const c={Critical:"priority-critical",High:"priority-high",Medium:"priority-medium",Low:"priority-low"}[p]||"";return`<span class="${c}">${p}</span>`}
function updateState(s){
  document.getElementById("zone").textContent=s.zone;
  document.getElementById("people").textContent=s.people;
  document.getElementById("injured").textContent=s.injured;
  document.getElementById("food").innerHTML=boolBadge(s.food_needed);
  document.getElementById("rescue").innerHTML=boolBadge(s.rescue_needed);
  document.getElementById("power").innerHTML=boolBadge(s.power_outage);
  document.getElementById("infra").innerHTML=boolBadge(s.infrastructure_damage);
  document.getElementById("disease").innerHTML=boolBadge(s.disease_outbreak);
  document.getElementById("step").textContent=s.step??"-";
  document.getElementById("max-steps").textContent=s.max_steps??"-";
}
function runStep(){
  const agent=document.getElementById("agent").value;
  document.getElementById("action").textContent="Thinking...";
  fetch("/step",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({agent})})
    .then(r=>r.json()).then(data=>{
      updateState(data.state);
      document.getElementById("action").textContent=ACTION_NAMES[data.action]||"Unknown";
      document.getElementById("reason").textContent=data.reason||"-";
      document.getElementById("reward").textContent=data.reward;
      document.getElementById("priority").innerHTML=priorityBadge(data.priority);
      document.getElementById("done").textContent=data.done?"Completed":"Running";
      const st=document.getElementById("ep-status");
      if(data.done){st.textContent="Done";st.className="badge badge-done";stopEpisode();}
      else{st.textContent="Running";st.className="badge badge-running";}
      totalScore+=data.reward;
      document.getElementById("score").textContent=Math.round(totalScore*10)/10;
    }).catch(e=>{document.getElementById("action").textContent="Error";console.error(e);});
}
function resetEnv(){
  stopEpisode();totalScore=0;
  const difficulty=document.getElementById("difficulty").value;
  fetch("/reset",{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify({difficulty})})
    .then(r=>r.json()).then(data=>{
      updateState(data.state);
      ["action","reason","reward","priority","done"].forEach(id=>document.getElementById(id).textContent="-");
      document.getElementById("score").textContent="0";
      document.getElementById("ep-status").textContent="Running";
      document.getElementById("ep-status").className="badge badge-running";
    });
}
function runEpisode(){stopEpisode();autoRunInterval=setInterval(runStep,800);}
function stopEpisode(){if(autoRunInterval){clearInterval(autoRunInterval);autoRunInterval=null;}}
window.addEventListener("DOMContentLoaded",()=>{
  fetch("/state").then(r=>r.json()).then(d=>updateState(d.state)).catch(()=>{});
});