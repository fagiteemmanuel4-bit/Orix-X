class b{container;tabsItemsContainer;tabsNavContainer;tabsContentContainer;tabButtons=null;tabNavs=null;tabContents=null;activeTabNumber=1;constructor(){this.container=document.querySelector(".hero-tabs-container"),this.tabsItemsContainer=document.querySelector(".hero-tabs-items"),this.tabsNavContainer=document.querySelector(".hero-tabs-nav"),this.tabsContentContainer=document.querySelector(".hero-tabs-content"),this.injectCSS(),this.init()}injectCSS(){const t=document.createElement("style");t.textContent=`
        .hero-tabs-nav .hero-tab-nav {
          flex: 1;
          transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
          overflow: hidden;
          margin: 0 !important;
          opacity: 0.6;
        }

        .hero-tabs-nav .hero-tab-nav[data-active="true"] {
          transform: translateY(-2px);
          opacity: 1;
        }

        .hero-tabs-nav .tab-button {
          width: 100%;
          border: none;
          padding: 1.5rem 0;
          color: var(--sl-color-text);
          background: transparent;
          cursor: pointer;
          display: flex;
          gap: 1rem;
          transition: all 0.3s ease;
          position: relative;
          overflow: hidden;
        }

        .hero-tabs-nav .tab-button:hover {
          background: var(--sl-color-gray-7);
        }

        .hero-tabs-nav .hero-tab-nav[data-active="true"] .tab-button::before {
          content: "";
          position: absolute;
          top: 0;
          left: 0;
          right: 0;
          height: 2px;
          background: var(--color-primary-gradient);
        }

        .hero-tabs-nav .tab-number {
          font-size: 1.1rem;
          background: var(--sl-color-black);
          color: var(--sl-color-light);
          width: 2rem;
          height: 2rem;
          border-radius: 50%;
          display: flex;
          align-items: center;
          justify-content: center;
          flex-shrink: 0;
          transition: all 0.3s ease;
        }

        .hero-tabs-nav .tab-content {
          text-align: left;
          flex-grow: 1;
        }

        .hero-tabs-nav .tab-title {
          font-size: 1.25rem;
          font-weight: 600;
          margin: 0 0 0.5rem 0;
          transition: all 0.3s ease;
        }

        .hero-tabs-nav .tab-subtitle {
          font-size: 0.875rem;
          opacity: 0.9;
          margin: 0;
          line-height: 1.4;
          transition: all 0.3s ease;
        }

        .hero-tabs-content {
          position: relative;
          
          overflow: hidden;
          background-color: var(--sl-color-black);
          margin-top: 3.5rem;
          padding: 0.6rem;
        }
        
        .hero-tabs-content .hero-tab-content {
         
          width: 100%;
          height: 100%;
          display: none;
          align-items: center;
          justify-content: center;
          padding: 2rem;
          transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
          margin-top:0px;
        }

        .hero-tabs-content .hero-tab-content[data-active="true"] {
          display: flex !important;
        }

        .hero-tabs-content .tab-image-container {
          width: 100%;
          position: relative;
        }

        .hero-tabs-content .tab-image {
          width: 100%;
          height: 100%;
          object-fit: contain;
          transition: transform 0.3s ease;
        }

        @media (max-width: 767px) {
          .hero-tabs-nav .tab-button { padding: 1rem; }
          .hero-tabs-nav .tab-number { font-size: 1rem; }
          .hero-tabs-nav .tab-title { font-size: 1.125rem; }
          .hero-tabs-nav .tab-subtitle { font-size: 0.8rem; }
          .hero-tabs-content { min-height: 300px; }
          .hero-tabs-content .hero-tab-content { padding: 1rem; }
        }
          @media (max-width: 560px) {
          .hero-tabs-content { min-height: auto; }

        }

      `,document.head.appendChild(t)}init(){!this.container||!this.tabsItemsContainer||setTimeout(()=>this.setupTabs(),500)}setupTabs(){const t=this.tabsItemsContainer?.querySelectorAll(".hero-tab-item");!t||t.length===0||(t.forEach((e,a)=>{const n=e.querySelector(".hero-tab-nav"),o=e.querySelector(".hero-tab-content");if(n&&o&&this.tabsNavContainer&&this.tabsContentContainer){const s=n.cloneNode(!0),r=o.cloneNode(!0),c=a===0;s.setAttribute("data-active",c.toString()),r.setAttribute("data-active",c.toString()),this.tabsNavContainer.appendChild(s),this.tabsContentContainer.appendChild(r)}}),setTimeout(()=>{this.bindEvents(),this.initializeVisibility()},100))}initializeVisibility(){if(!this.tabsContentContainer)return;this.tabContents=this.tabsContentContainer.querySelectorAll(".hero-tab-content"),this.tabContents.forEach(e=>{e.style.display="none"});const t=this.tabsContentContainer.querySelector('[data-panel="1"]');t&&(t.style.display="flex")}bindEvents(){!this.tabsNavContainer||!this.tabsContentContainer||(this.tabButtons=this.tabsNavContainer.querySelectorAll(".tab-button"),this.tabNavs=this.tabsNavContainer.querySelectorAll(".hero-tab-nav"),this.tabContents=this.tabsContentContainer.querySelectorAll(".hero-tab-content"),this.tabButtons.length!==0&&(this.tabButtons.forEach(t=>{t.addEventListener("click",e=>{e.preventDefault();const a=parseInt(t.dataset.tab||"1");this.switchTab(a)}),t.addEventListener("keydown",e=>{const a=e.key;if(a==="Enter"||a===" "){e.preventDefault();const n=parseInt(t.dataset.tab||"1");this.switchTab(n)}})}),this.addKeyboardNavigation(),this.addEntranceAnimations()))}switchTab(t){t!==this.activeTabNumber&&(this.deactivateCurrentTab(),this.activateTab(t),this.activeTabNumber=t,this.container?.dispatchEvent(new CustomEvent("tabChanged",{detail:{activeTab:t}})))}deactivateCurrentTab(){this.tabNavs?.forEach(t=>{t.setAttribute("data-active","false"),t.classList.remove("active")}),this.tabContents?.forEach(t=>{t.setAttribute("data-active","false"),t.classList.remove("active","fade-in"),t.style.display="none"})}activateTab(t){const e=this.tabsNavContainer?.querySelector(`[data-tab="${t}"]`)?.closest(".hero-tab-nav");e&&(e.setAttribute("data-active","true"),e.classList.add("active"));const a=this.tabsContentContainer?.querySelector(`[data-panel="${t}"]`);a&&(a.style.display="flex",a.setAttribute("data-active","true"),a.classList.add("active","fade-in")),this.tabsNavContainer?.querySelector(`[data-tab="${t}"]`)?.focus()}addKeyboardNavigation(){document.addEventListener("keydown",t=>{if(!this.container?.contains(document.activeElement))return;let e=this.activeTabNumber;const a=this.tabButtons?.length||0;switch(t.key){case"ArrowRight":case"ArrowDown":t.preventDefault(),e=this.activeTabNumber<a?this.activeTabNumber+1:1;break;case"ArrowLeft":case"ArrowUp":t.preventDefault(),e=this.activeTabNumber>1?this.activeTabNumber-1:a;break;case"Home":t.preventDefault(),e=1;break;case"End":t.preventDefault(),e=a;break}e!==this.activeTabNumber&&this.switchTab(e)})}addEntranceAnimations(){this.tabNavs?.forEach((t,e)=>{setTimeout(()=>t.classList.add("animate-in"),e*100)})}goToTab(t){const e=this.tabButtons?.length||0;t>=1&&t<=e&&this.switchTab(t)}getActiveTab(){return this.activeTabNumber}}document.addEventListener("DOMContentLoaded",()=>{const i=new b;window.heroTabs=i});
