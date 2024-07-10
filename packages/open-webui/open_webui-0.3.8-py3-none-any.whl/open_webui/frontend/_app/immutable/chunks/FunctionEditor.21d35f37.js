import{s as De,p as te,f as r,a as H,l as me,g as d,h as x,R as ie,c as q,m as he,d as m,j as i,i as le,r as a,Q as O,u as G,O as Me,n as pe,W as _e,v as Te,V as Ve,P as Ce,w as Fe,C as Pe}from"./scheduler.8ceb707f.js";import{S as He,i as qe,f as ve,b as ge,d as be,m as ye,a as we,t as xe,e as Ie}from"./index.07e72a31.js";import{g as Ae}from"./navigation.1979c3c4.js";import{C as Be}from"./CodeEditor.e80b5ad2.js";import{C as Le}from"./ConfirmDialog.aad7ae0e.js";function Ne(t){let l,s=`<div class="bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"><div>Please carefully review the following warnings:</div> <ul class="mt-1 list-disc pl-4 text-xs"><li>Functions allow arbitrary code execution.</li> <li>Do not install functions from sources you do not fully trust.</li></ul></div> <div class="my-3">I acknowledge that I have read and I understand the implications of my action. I am aware of
			the risks associated with executing arbitrary code and I have verified the trustworthiness of
			the source.</div>`;return{c(){l=r("div"),l.innerHTML=s,this.h()},l(o){l=d(o,"DIV",{class:!0,"data-svelte-h":!0}),ie(l)!=="svelte-1pkea5f"&&(l.innerHTML=s),this.h()},h(){i(l,"class","text-sm text-gray-500")},m(o,k){le(o,l,k)},p:Pe,d(o){o&&m(l)}}}function Ue(t){let l,s,o,k,p,_,A='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clip-rule="evenodd"></path></svg>',T,I,w=t[8].t("Back")+"",v,V,f,h,E,g,B,c,S,b,j,F,y,z,W,D,C,J=`<div class="text-xs text-gray-500 line-clamp-2"><span class="font-semibold dark:text-gray-200">Warning:</span> Functions allow
							arbitrary code execution <br/>—
							<span class="font-medium dark:text-gray-400">don&#39;t install random functions from sources you don&#39;t trust.</span></div>`,n,L,R=t[8].t("Save")+"",K,X,M,se,N,ne,ae;function ke(e){t[17](e)}let oe={boilerplate:t[10]};t[3]!==void 0&&(oe.value=t[3]),y=new Be({props:oe}),te.push(()=>ve(y,"value",ke)),t[18](y),y.$on("save",t[19]);function Ee(e){t[22](e)}let re={$$slots:{default:[Ne]},$$scope:{ctx:t}};return t[6]!==void 0&&(re.show=t[6]),M=new Le({props:re}),te.push(()=>ve(M,"show",Ee)),M.$on("confirm",t[23]),{c(){l=r("div"),s=r("div"),o=r("form"),k=r("div"),p=r("button"),_=r("div"),_.innerHTML=A,T=H(),I=r("div"),v=me(w),V=H(),f=r("div"),h=r("div"),E=r("div"),g=r("input"),B=H(),c=r("input"),S=H(),b=r("input"),j=H(),F=r("div"),ge(y.$$.fragment),W=H(),D=r("div"),C=r("div"),C.innerHTML=J,n=H(),L=r("button"),K=me(R),X=H(),ge(M.$$.fragment),this.h()},l(e){l=d(e,"DIV",{class:!0});var u=x(l);s=d(u,"DIV",{class:!0});var Q=x(s);o=d(Q,"FORM",{class:!0});var P=x(o);k=d(P,"DIV",{class:!0});var de=x(k);p=d(de,"BUTTON",{class:!0,type:!0});var Y=x(p);_=d(Y,"DIV",{class:!0,"data-svelte-h":!0}),ie(_)!=="svelte-1t52rj4"&&(_.innerHTML=A),T=q(Y),I=d(Y,"DIV",{class:!0});var ue=x(I);v=he(ue,w),ue.forEach(m),Y.forEach(m),de.forEach(m),V=q(P),f=d(P,"DIV",{class:!0});var U=x(f);h=d(U,"DIV",{class:!0});var Z=x(h);E=d(Z,"DIV",{class:!0});var $=x(E);g=d($,"INPUT",{class:!0,type:!0,placeholder:!0}),B=q($),c=d($,"INPUT",{class:!0,type:!0,placeholder:!0}),$.forEach(m),S=q(Z),b=d(Z,"INPUT",{class:!0,type:!0,placeholder:!0}),Z.forEach(m),j=q(U),F=d(U,"DIV",{class:!0});var fe=x(F);be(y.$$.fragment,fe),fe.forEach(m),W=q(U),D=d(U,"DIV",{class:!0});var ee=x(D);C=d(ee,"DIV",{class:!0,"data-svelte-h":!0}),ie(C)!=="svelte-11344qq"&&(C.innerHTML=J),n=q(ee),L=d(ee,"BUTTON",{class:!0,type:!0});var ce=x(L);K=he(ce,R),ce.forEach(m),ee.forEach(m),U.forEach(m),P.forEach(m),Q.forEach(m),u.forEach(m),X=q(e),be(M.$$.fragment,e),this.h()},h(){i(_,"class","self-center"),i(I,"class","self-center font-medium text-sm"),i(p,"class","flex space-x-1"),i(p,"type","button"),i(k,"class","mb-2.5"),i(g,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),i(g,"type","text"),i(g,"placeholder","Function Name (e.g. My Filter)"),g.required=!0,i(c,"class","w-full px-3 py-2 text-sm font-medium disabled:text-gray-300 dark:disabled:text-gray-700 bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),i(c,"type","text"),i(c,"placeholder","Function ID (e.g. my_filter)"),c.required=!0,c.disabled=t[4],i(E,"class","flex gap-2 w-full"),i(b,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),i(b,"type","text"),i(b,"placeholder","Function Description (e.g. A filter to remove profanity from text)"),b.required=!0,i(h,"class","w-full mb-2 flex flex-col gap-1.5"),i(F,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),i(C,"class","flex-1 pr-3"),i(L,"class","px-3 py-1.5 text-sm font-medium bg-emerald-600 hover:bg-emerald-700 text-gray-50 transition rounded-lg"),i(L,"type","submit"),i(D,"class","pb-3 flex justify-between"),i(f,"class","flex flex-col flex-1 overflow-auto h-0 rounded-lg"),i(o,"class","flex flex-col max-h-[100dvh] h-full"),i(s,"class","mx-auto w-full md:px-0 h-full"),i(l,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(e,u){le(e,l,u),a(l,s),a(s,o),a(o,k),a(k,p),a(p,_),a(p,T),a(p,I),a(I,v),a(o,V),a(o,f),a(f,h),a(h,E),a(E,g),O(g,t[0]),a(E,B),a(E,c),O(c,t[1]),a(h,S),a(h,b),O(b,t[2].description),a(f,j),a(f,F),ye(y,F,null),a(f,W),a(f,D),a(D,C),a(D,n),a(D,L),a(L,K),t[20](o),le(e,X,u),ye(M,e,u),N=!0,ne||(ae=[G(p,"click",t[13]),G(g,"input",t[14]),G(c,"input",t[15]),G(b,"input",t[16]),G(o,"submit",Me(t[21]))],ne=!0)},p(e,[u]){(!N||u&256)&&w!==(w=e[8].t("Back")+"")&&pe(v,w),u&1&&g.value!==e[0]&&O(g,e[0]),(!N||u&16)&&(c.disabled=e[4]),u&2&&c.value!==e[1]&&O(c,e[1]),u&4&&b.value!==e[2].description&&O(b,e[2].description);const Q={};!z&&u&8&&(z=!0,Q.value=e[3],_e(()=>z=!1)),y.$set(Q),(!N||u&256)&&R!==(R=e[8].t("Save")+"")&&pe(K,R);const P={};u&268435456&&(P.$$scope={dirty:u,ctx:e}),!se&&u&64&&(se=!0,P.show=e[6],_e(()=>se=!1)),M.$set(P)},i(e){N||(we(y.$$.fragment,e),we(M.$$.fragment,e),N=!0)},o(e){xe(y.$$.fragment,e),xe(M.$$.fragment,e),N=!1},d(e){e&&(m(l),m(X)),t[18](null),Ie(y),t[20](null),Ie(M,e),ne=!1,Te(ae)}}}function Oe(t,l,s){let o;const k=Ve(),p=Ce("i18n");Fe(t,p,n=>s(8,o=n));let _=null,A=!1,{edit:T=!1}=l,{clone:I=!1}=l,{id:w=""}=l,{name:v=""}=l,{meta:V={description:""}}=l,{content:f=""}=l,h,E=`"""
title: Example Filter
author: open-webui
author_url: https://github.com/open-webui
funding_url: https://github.com/open-webui
version: 0.1
"""

from pydantic import BaseModel, Field
from typing import Optional


class Filter:
    class Valves(BaseModel):
        priority: int = Field(
            default=0, description="Priority level for the filter operations."
        )
        max_turns: int = Field(
            default=8, description="Maximum allowable conversation turns for a user."
        )
        pass

    class UserValves(BaseModel):
        max_turns: int = Field(
            default=4, description="Maximum allowable conversation turns for a user."
        )
        pass

    def __init__(self):
        # Indicates custom file handling logic. This flag helps disengage default routines in favor of custom
        # implementations, informing the WebUI to defer file-related operations to designated methods within this class.
        # Alternatively, you can remove the files directly from the body in from the inlet hook
        # self.file_handler = True

        # Initialize 'valves' with specific configurations. Using 'Valves' instance helps encapsulate settings,
        # which ensures settings are managed cohesively and not confused with operational flags like 'file_handler'.
        self.valves = self.Valves()
        pass

    def inlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify the request body or validate it before processing by the chat completion API.
        # This function is the pre-processor for the API where various checks on the input can be performed.
        # It can also modify the request before sending it to the API.
        print(f"inlet:{__name__}")
        print(f"inlet:body:{body}")
        print(f"inlet:user:{__user__}")

        if __user__.get("role", "admin") in ["user", "admin"]:
            messages = body.get("messages", [])

            max_turns = min(__user__["valves"].max_turns, self.valves.max_turns)
            if len(messages) > max_turns:
                raise Exception(
                    f"Conversation turn limit exceeded. Max turns: {max_turns}"
                )

        return body

    def outlet(self, body: dict, __user__: Optional[dict] = None) -> dict:
        # Modify or analyze the response body after processing by the API.
        # This function is the post-processor for the API, which can be used to modify the response
        # or perform additional checks and analytics.
        print(f"outlet:{__name__}")
        print(f"outlet:body:{body}")
        print(f"outlet:user:{__user__}")

        return body
`;const g=async()=>{k("save",{id:w,name:v,meta:V,content:f})},B=async()=>{h&&await h.formatPythonCodeHandler()&&(console.log("Code formatted successfully"),g())},c=()=>{Ae("/workspace/functions")};function S(){v=this.value,s(0,v)}function b(){w=this.value,s(1,w),s(0,v),s(4,T),s(12,I)}function j(){V.description=this.value,s(2,V)}function F(n){f=n,s(3,f)}function y(n){te[n?"unshift":"push"](()=>{h=n,s(7,h)})}const z=()=>{_&&_.requestSubmit()};function W(n){te[n?"unshift":"push"](()=>{_=n,s(5,_)})}const D=()=>{T?B():s(6,A=!0)};function C(n){A=n,s(6,A)}const J=()=>{B()};return t.$$set=n=>{"edit"in n&&s(4,T=n.edit),"clone"in n&&s(12,I=n.clone),"id"in n&&s(1,w=n.id),"name"in n&&s(0,v=n.name),"meta"in n&&s(2,V=n.meta),"content"in n&&s(3,f=n.content)},t.$$.update=()=>{t.$$.dirty&4113&&v&&!T&&!I&&s(1,w=v.replace(/\s+/g,"_").toLowerCase())},[v,w,V,f,T,_,A,h,o,p,E,B,I,c,S,b,j,F,y,z,W,D,C,J]}class Qe extends He{constructor(l){super(),qe(this,l,Oe,Ue,De,{edit:4,clone:12,id:1,name:0,meta:2,content:3})}}export{Qe as F};
//# sourceMappingURL=FunctionEditor.21d35f37.js.map
