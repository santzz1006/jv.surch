/* Locally vendored GSAP. Content remains usable when scripts are unavailable. */
if(window.gsap&&window.ScrollTrigger){
  gsap.registerPlugin(ScrollTrigger);
  const media=gsap.matchMedia();
  media.add('(prefers-reduced-motion: no-preference)',()=>{
    gsap.from('.logo',{y:-10,opacity:0,duration:.55,ease:'power2.out',clearProps:'all'});
    gsap.from('.market-hero .banner',{y:24,opacity:0,stagger:.1,duration:.7,ease:'power2.out',clearProps:'all'});
    gsap.utils.toArray('.promo-band,.collection-toolbar').forEach(section=>gsap.from(section,{y:28,opacity:0,duration:.7,clearProps:'all',scrollTrigger:{trigger:section,start:'top 94%',once:true}}));
    let gridTween;
    const animateGrid=()=>{gridTween?.kill();const cards=document.querySelectorAll('#grid>.product-cell');gsap.set(cards,{clearProps:'all'});if(cards.length)gridTween=gsap.from(cards,{y:16,opacity:0,stagger:.025,duration:.4,clearProps:'all'});ScrollTrigger.refresh();};
    const observer=new MutationObserver(animateGrid);observer.observe(document.getElementById('grid'),{childList:true});
    return ()=>{observer.disconnect();gridTween?.kill();gsap.set('#grid>.product-cell',{clearProps:'all'});};
  });
}
