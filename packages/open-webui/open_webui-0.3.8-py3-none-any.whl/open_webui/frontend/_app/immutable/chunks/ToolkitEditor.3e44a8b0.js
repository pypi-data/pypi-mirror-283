import{s as Ie,p as te,f as l,a as M,l as me,g as u,h as x,R as se,c as A,m as _e,d as m,j as s,i as ne,r as o,Q as S,u as Y,O as De,n as he,W as pe,v as Ce,P as qe,w as Pe,V as He,C as Ve}from"./scheduler.8ceb707f.js";import{S as Me,i as Ae,f as ge,b as ve,d as ye,m as we,a as be,t as xe,e as ke}from"./index.07e72a31.js";import{C as Ue}from"./CodeEditor.e80b5ad2.js";import{g as je}from"./navigation.1979c3c4.js";import{C as Le}from"./ConfirmDialog.aad7ae0e.js";function Ne(t){let n,a=`<div class="bg-yellow-500/20 text-yellow-700 dark:text-yellow-200 rounded-lg px-4 py-3"><div>Please carefully review the following warnings:</div> <ul class="mt-1 list-disc pl-4 text-xs"><li>Tools have a function calling system that allows arbitrary code execution.</li> <li>Do not install tools from sources you do not fully trust.</li></ul></div> <div class="my-3">I acknowledge that I have read and I understand the implications of my action. I am aware of
			the risks associated with executing arbitrary code and I have verified the trustworthiness of
			the source.</div>`;return{c(){n=l("div"),n.innerHTML=a,this.h()},l(i){n=u(i,"DIV",{class:!0,"data-svelte-h":!0}),se(n)!=="svelte-zyc2yl"&&(n.innerHTML=a),this.h()},h(){s(n,"class","text-sm text-gray-500")},m(i,k){ne(i,n,k)},p:Ve,d(i){i&&m(n)}}}function Oe(t){let n,a,i,k,w,h,U='<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 20 20" fill="currentColor" class="w-4 h-4"><path fill-rule="evenodd" d="M17 10a.75.75 0 01-.75.75H5.612l4.158 3.96a.75.75 0 11-1.04 1.08l-5.5-5.25a.75.75 0 010-1.08l5.5-5.25a.75.75 0 111.04 1.08L5.612 9.25H16.25A.75.75 0 0117 10z" clip-rule="evenodd"></path></svg>',C,E,b=t[8].t("Back")+"",p,q,c,_,T,g,j,f,B,v,R,H,y,W,F,I,P,z=`<div class="text-xs text-gray-500 line-clamp-2"><span class="font-semibold dark:text-gray-200">Warning:</span> Tools are a function
							calling system with arbitrary code execution <br/>—
							<span class="font-medium dark:text-gray-400">don&#39;t install random tools from sources you don&#39;t trust.</span></div>`,r,L,G=t[8].t("Save")+"",Q,J,D,ae,N,re,oe;function Ee(e){t[17](e)}let ie={boilerplate:t[10]};t[3]!==void 0&&(ie.value=t[3]),y=new Ue({props:ie}),te.push(()=>ge(y,"value",Ee)),t[18](y),y.$on("save",t[19]);function Te(e){t[22](e)}let le={$$slots:{default:[Ne]},$$scope:{ctx:t}};return t[6]!==void 0&&(le.show=t[6]),D=new Le({props:le}),te.push(()=>ge(D,"show",Te)),D.$on("confirm",t[23]),{c(){n=l("div"),a=l("div"),i=l("form"),k=l("div"),w=l("button"),h=l("div"),h.innerHTML=U,C=M(),E=l("div"),p=me(b),q=M(),c=l("div"),_=l("div"),T=l("div"),g=l("input"),j=M(),f=l("input"),B=M(),v=l("input"),R=M(),H=l("div"),ve(y.$$.fragment),F=M(),I=l("div"),P=l("div"),P.innerHTML=z,r=M(),L=l("button"),Q=me(G),J=M(),ve(D.$$.fragment),this.h()},l(e){n=u(e,"DIV",{class:!0});var d=x(n);a=u(d,"DIV",{class:!0});var K=x(a);i=u(K,"FORM",{class:!0});var V=x(i);k=u(V,"DIV",{class:!0});var ue=x(k);w=u(ue,"BUTTON",{class:!0,type:!0});var X=x(w);h=u(X,"DIV",{class:!0,"data-svelte-h":!0}),se(h)!=="svelte-1t52rj4"&&(h.innerHTML=U),C=A(X),E=u(X,"DIV",{class:!0});var de=x(E);p=_e(de,b),de.forEach(m),X.forEach(m),ue.forEach(m),q=A(V),c=u(V,"DIV",{class:!0});var O=x(c);_=u(O,"DIV",{class:!0});var Z=x(_);T=u(Z,"DIV",{class:!0});var $=x(T);g=u($,"INPUT",{class:!0,type:!0,placeholder:!0}),j=A($),f=u($,"INPUT",{class:!0,type:!0,placeholder:!0}),$.forEach(m),B=A(Z),v=u(Z,"INPUT",{class:!0,type:!0,placeholder:!0}),Z.forEach(m),R=A(O),H=u(O,"DIV",{class:!0});var ce=x(H);ye(y.$$.fragment,ce),ce.forEach(m),F=A(O),I=u(O,"DIV",{class:!0});var ee=x(I);P=u(ee,"DIV",{class:!0,"data-svelte-h":!0}),se(P)!=="svelte-ons8ff"&&(P.innerHTML=z),r=A(ee),L=u(ee,"BUTTON",{class:!0,type:!0});var fe=x(L);Q=_e(fe,G),fe.forEach(m),ee.forEach(m),O.forEach(m),V.forEach(m),K.forEach(m),d.forEach(m),J=A(e),ye(D.$$.fragment,e),this.h()},h(){s(h,"class","self-center"),s(E,"class","self-center font-medium text-sm"),s(w,"class","flex space-x-1"),s(w,"type","button"),s(k,"class","mb-2.5"),s(g,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),s(g,"type","text"),s(g,"placeholder","Toolkit Name (e.g. My ToolKit)"),g.required=!0,s(f,"class","w-full px-3 py-2 text-sm font-medium disabled:text-gray-300 dark:disabled:text-gray-700 bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),s(f,"type","text"),s(f,"placeholder","Toolkit ID (e.g. my_toolkit)"),f.required=!0,f.disabled=t[4],s(T,"class","flex gap-2 w-full"),s(v,"class","w-full px-3 py-2 text-sm font-medium bg-gray-50 dark:bg-gray-850 dark:text-gray-200 rounded-lg outline-none"),s(v,"type","text"),s(v,"placeholder","Toolkit Description (e.g. A toolkit for performing various operations)"),v.required=!0,s(_,"class","w-full mb-2 flex flex-col gap-1.5"),s(H,"class","mb-2 flex-1 overflow-auto h-0 rounded-lg"),s(P,"class","flex-1 pr-3"),s(L,"class","px-3 py-1.5 text-sm font-medium bg-emerald-600 hover:bg-emerald-700 text-gray-50 transition rounded-lg"),s(L,"type","submit"),s(I,"class","pb-3 flex justify-between"),s(c,"class","flex flex-col flex-1 overflow-auto h-0 rounded-lg"),s(i,"class","flex flex-col max-h-[100dvh] h-full"),s(a,"class","mx-auto w-full md:px-0 h-full"),s(n,"class","flex flex-col justify-between w-full overflow-y-auto h-full")},m(e,d){ne(e,n,d),o(n,a),o(a,i),o(i,k),o(k,w),o(w,h),o(w,C),o(w,E),o(E,p),o(i,q),o(i,c),o(c,_),o(_,T),o(T,g),S(g,t[0]),o(T,j),o(T,f),S(f,t[1]),o(_,B),o(_,v),S(v,t[2].description),o(c,R),o(c,H),we(y,H,null),o(c,F),o(c,I),o(I,P),o(I,r),o(I,L),o(L,Q),t[20](i),ne(e,J,d),we(D,e,d),N=!0,re||(oe=[Y(w,"click",t[13]),Y(g,"input",t[14]),Y(f,"input",t[15]),Y(v,"input",t[16]),Y(i,"submit",De(t[21]))],re=!0)},p(e,[d]){(!N||d&256)&&b!==(b=e[8].t("Back")+"")&&he(p,b),d&1&&g.value!==e[0]&&S(g,e[0]),(!N||d&16)&&(f.disabled=e[4]),d&2&&f.value!==e[1]&&S(f,e[1]),d&4&&v.value!==e[2].description&&S(v,e[2].description);const K={};!W&&d&8&&(W=!0,K.value=e[3],pe(()=>W=!1)),y.$set(K),(!N||d&256)&&G!==(G=e[8].t("Save")+"")&&he(Q,G);const V={};d&134217728&&(V.$$scope={dirty:d,ctx:e}),!ae&&d&64&&(ae=!0,V.show=e[6],pe(()=>ae=!1)),D.$set(V)},i(e){N||(be(y.$$.fragment,e),be(D.$$.fragment,e),N=!0)},o(e){xe(y.$$.fragment,e),xe(D.$$.fragment,e),N=!1},d(e){e&&(m(n),m(J)),t[18](null),ke(y),t[20](null),ke(D,e),re=!1,Ce(oe)}}}function Se(t,n,a){let i;const k=qe("i18n");Pe(t,k,r=>a(8,i=r));const w=He();let h=null,U=!1,{edit:C=!1}=n,{clone:E=!1}=n,{id:b=""}=n,{name:p=""}=n,{meta:q={description:""}}=n,{content:c=""}=n,_,T=`import os
import requests
from datetime import datetime


class Tools:
    def __init__(self):
        pass

    # Add your custom tools using pure Python code here, make sure to add type hints
    # Use Sphinx-style docstrings to document your tools, they will be used for generating tools specifications
    # Please refer to function_calling_filter_pipeline.py file from pipelines project for an example

    def get_user_name_and_email_and_id(self, __user__: dict = {}) -> str:
        """
        Get the user name, Email and ID from the user object.
        """

        # Do not include :param for __user__ in the docstring as it should not be shown in the tool's specification
        # The session user object will be passed as a parameter when the function is called

        print(__user__)
        result = ""

        if "name" in __user__:
            result += f"User: {__user__['name']}"
        if "id" in __user__:
            result += f" (ID: {__user__['id']})"
        if "email" in __user__:
            result += f" (Email: {__user__['email']})"

        if result == "":
            result = "User: Unknown"

        return result

    def get_current_time(self) -> str:
        """
        Get the current time in a more human-readable format.
        :return: The current time.
        """

        now = datetime.now()
        current_time = now.strftime("%I:%M:%S %p")  # Using 12-hour format with AM/PM
        current_date = now.strftime(
            "%A, %B %d, %Y"
        )  # Full weekday, month name, day, and year

        return f"Current Date and Time = {current_date}, {current_time}"

    def calculator(self, equation: str) -> str:
        """
        Calculate the result of an equation.
        :param equation: The equation to calculate.
        """

        # Avoid using eval in production code
        # https://nedbatchelder.com/blog/201206/eval_really_is_dangerous.html
        try:
            result = eval(equation)
            return f"{equation} = {result}"
        except Exception as e:
            print(e)
            return "Invalid equation"

    def get_current_weather(self, city: str) -> str:
        """
        Get the current weather for a given city.
        :param city: The name of the city to get the weather for.
        :return: The current weather information or an error message.
        """
        api_key = os.getenv("OPENWEATHER_API_KEY")
        if not api_key:
            return (
                "API key is not set in the environment variable 'OPENWEATHER_API_KEY'."
            )

        base_url = "http://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": city,
            "appid": api_key,
            "units": "metric",  # Optional: Use 'imperial' for Fahrenheit
        }

        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx and 5xx)
            data = response.json()

            if data.get("cod") != 200:
                return f"Error fetching weather data: {data.get('message')}"

            weather_description = data["weather"][0]["description"]
            temperature = data["main"]["temp"]
            humidity = data["main"]["humidity"]
            wind_speed = data["wind"]["speed"]

            return f"Weather in {city}: {temperature}°C"
        except requests.RequestException as e:
            return f"Error fetching weather data: {str(e)}"
`;const g=async()=>{w("save",{id:b,name:p,meta:q,content:c})},j=async()=>{_&&await _.formatPythonCodeHandler()&&(console.log("Code formatted successfully"),g())},f=()=>{je("/workspace/tools")};function B(){p=this.value,a(0,p)}function v(){b=this.value,a(1,b),a(0,p),a(4,C),a(12,E)}function R(){q.description=this.value,a(2,q)}function H(r){c=r,a(3,c)}function y(r){te[r?"unshift":"push"](()=>{_=r,a(7,_)})}const W=()=>{h&&h.requestSubmit()};function F(r){te[r?"unshift":"push"](()=>{h=r,a(5,h)})}const I=()=>{C?j():a(6,U=!0)};function P(r){U=r,a(6,U)}const z=()=>{j()};return t.$$set=r=>{"edit"in r&&a(4,C=r.edit),"clone"in r&&a(12,E=r.clone),"id"in r&&a(1,b=r.id),"name"in r&&a(0,p=r.name),"meta"in r&&a(2,q=r.meta),"content"in r&&a(3,c=r.content)},t.$$.update=()=>{t.$$.dirty&4113&&p&&!C&&!E&&a(1,b=p.replace(/\s+/g,"_").toLowerCase())},[p,b,q,c,C,h,U,_,i,k,T,j,E,f,B,v,R,H,y,W,F,I,P,z]}class Ke extends Me{constructor(n){super(),Ae(this,n,Se,Oe,Ie,{edit:4,clone:12,id:1,name:0,meta:2,content:3})}}export{Ke as T};
//# sourceMappingURL=ToolkitEditor.3e44a8b0.js.map
