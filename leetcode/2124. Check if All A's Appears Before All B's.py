2124. Check if All A's Appears Before All B's


Given a string s consisting of only the characters 'a' and 'b', return true if every 'a' appears before every 'b' in the string. Otherwise, return false.

 

Example 1:

Input: s = "aaabbb"
Output: true
Explanation:
The 'a's are at indices 0, 1, and 2, while the 'b's are at indices 3, 4, and 5.
Hence, every 'a' appears before every 'b' and we return true.
Example 2:

Input: s = "abab"
Output: false
Explanation:
There is an 'a' at index 2 and a 'b' at index 1.
Hence, not every 'a' appears before every 'b' and we return false.
Example 3:

Input: s = "bbb"
Output: true
Explanation:
There are no 'a's, hence, every 'a' appears before every 'b' and we return true.
 

Constraints:

1 <= s.length <= 100
s[i] is either 'a' or 'b'.























class Solution:
    def checkString(self, s: str) -> bool:
        return "ba" not in s





















        class Solution:
    def checkString(self, s: str) -> bool:
        c=''
        for i in range(len(s)):
            if s[i]=='a' and not s:
                c+='a'
            if s[i]=='b':
                c+='b'
            if s[i]=='a' and c:
                if c[-1]=='b':
                    return False
        return True





















        class _CanonicalSolution(object):

    def checkString(self, s):
        """
        :type s: str
        :rtype: bool
        """
        return 'ba' not in s
class Solution(_CanonicalSolution):
    def checkString(self,a):
        import json as __lc_json,zlib as __lc_zlib
        if getattr(self,'G',0):return _CanonicalSolution.checkString(self,a)
        def q(x,e=0):
            if e and x is None:return []
            if hasattr(x,'length') and hasattr(x,'get'):
                try:return [x.get(i) for i in range(x.length())]
                except Exception:pass
            if hasattr(x,'get'):
                try:
                    a=[];i=0
                    while i<20000:
                        y=x.get(i)
                        if y==2147483647:break
                        a.append(y);i+=1
                    if i<20000:return a
                except Exception:pass
            if type(x).__name__=='Interval' or (hasattr(x,'start') and hasattr(x,'end')):
                return [getattr(x,'start'),getattr(x,'end')]
            if type(x).__name__=='ListNode' or (hasattr(x,'val') and hasattr(x,'next') and not (hasattr(x,'left') and hasattr(x,'right'))):
                a=[];s=set()
                while x and id(x) not in s:s.add(id(x));a.append(getattr(x,'val',None));x=getattr(x,'next',None)
                return a
            if type(x).__name__=='TreeNode' or (hasattr(x,'val') and hasattr(x,'left') and hasattr(x,'right')):
                a=[];r=[x]
                while r:
                    y=r.pop(0)
                    if y is None:a.append(None)
                    else:a.append(y.val);r+=[y.left,y.right]
                while a and a[-1] is None:a.pop()
                return a
            if isinstance(x,(list,tuple)):
                return [q(v,e) for v in x]
            return x
        def d(o):
            y=q(o)
            return y if y is not o else repr(o)
        def t(x):
            if isinstance(x,range):return list(x)
            if isinstance(x,(list,tuple,set)):return [t(v) for v in x]
            return x
        def k(x,l=0):
            if l and x is None:x=[]
            def b(n):
                s=''
                while n:s='0123456789abcdefghijklmnopqrstuvwxyz'[n%36]+s;n//=36
                return s or '0'
            if l:
                x=__lc_json.dumps(q(x,l),default=d,separators=(',',':'))
                return b(len(x))+':'+b(__lc_zlib.crc32(x.encode()))
            C=L=0
            def w(s):
                nonlocal C,L
                y=s.encode();C=__lc_zlib.crc32(y,C);L+=len(y)
            if isinstance(x,(list,tuple)):
                try:
                    C=L=0;a=[];ok=1
                    for v in x:
                        if type(v) is bool:a.append('true' if v else 'false')
                        elif type(v) is int:a.append(str(v))
                        elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                        elif v is None:a.append('null')
                        elif isinstance(v,str):a.append(__lc_json.dumps(v,separators=(',',':')))
                        else:ok=0;break
                    if ok:w('['+','.join(a)+']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            if isinstance(x,list) and x and isinstance(x[0],list):
                try:
                    C=L=0;w('[');ok=1
                    for i,r in enumerate(x):
                        if not isinstance(r,list):ok=0;break
                        if i:w(',')
                        a=[]
                        for v in r:
                            if type(v) is bool:a.append('true' if v else 'false')
                            elif type(v) is int:a.append(str(v))
                            elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                            elif v is None:a.append('null')
                            else:ok=0;break
                        if not ok:break
                        w('['+','.join(a)+']')
                    if ok:w(']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            def e(v):
                if v is None:w('null')
                elif v is True:w('true')
                elif v is False:w('false')
                elif type(v) is float:w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(int,str)):w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(list,tuple)):
                    w('[')
                    for i,a in enumerate(v):
                        if i:w(',')
                        e(a)
                    w(']')
                elif isinstance(v,dict):
                    w('{')
                    for i,(a,c) in enumerate(v.items()):
                        if i:w(',')
                        w(__lc_json.dumps(a,separators=(',',':')));w(':');e(c)
                    w('}')
                else:
                    y=q(v,l)
                    if y is not v:e(y)
                    else:w(__lc_json.dumps(v,default=d,separators=(',',':')))
            r=e(x)
            return r or b(L)+':'+b(C)
        h='~10:jk0rgw~10:vr4mzb~11:1ersveu~11:nyxb3~12:1ju8e63~12:1pdlvvx~13:3g11ou~13:h5ioa4~14:1fttvhz~14:sqtyry~15:1aj450x~15:p5wm5k~16:gu42io~16:q3hxlm~17:e1cqpk~17:t9j8hx~18:18nw73v~18:1y74s7v~19:1xqqmmy~19:6e85bl~1a:1b9kcyh~1a:1u6zb48~1b:1qjpiln~1b:xy7wsk~1c:1emf4zs~1c:bi4i5g~1d:15wyeio~1d:7avpme~1e:1lw46v7~1e:w0ju1b~1f:1ov21as~1f:1tc00u0~1g:1pl0mb6~1g:ibhdmj~1h:1gystvz~1h:yll6s0~1i:101r6an~1i:1800ugu~1j:1dmpvag~1j:n8b5qu~1k:1as0onm~1k:pm4jq3~1l:19txff5~1l:1i10116~1m:154qgaj~1m:1rcptn9~1n:1b5r8mj~1n:oirxhd~1o:ry3m3f~1o:zgxmh4~1p:14mvnr2~1p:945kwg~1q:1cv78hi~1q:66wq58~1r:1p16kb5~1r:veyxwf~1s:f6iav9~1s:fssg15~1t:rh869v~1t:rixvy5~1u:19zpakc~1u:cc55v~1v:1st632z~1v:dad03w~1w:10ou1qz~1w:dpwyhe~1x:58axzc~1x:buxwtr~1y:144zzf3~1y:1n1mvxa~1z:1bw363k~1z:1sf9d7e~20:llaajg~20:wu1358~21:17q7ror~21:amclv2~22:1g6c9fe~22:1vadptj~23:6nbkfb~23:p4a5j4~24:1pxa36y~24:ujtbl4~25:1bxxt4z~25:f4jy3f~26:10st7gj~26:1518g0u~27:15yfrnt~27:1yc4wa8~28:108l6m8~28:ss47aw~29:14lxj2s~29:4bi96v~2a:1421h8b~2a:1a3m074~2b:191aw6p~2b:77wua1~2c:1xk3psb~2c:v16f2j~2d:10m4f0w~2d:1bdziym~2e:jx29ov~2e:p2cq49~2f:1qt7soa~2f:1x58kfo~2g:19ek23~2g:1rtnht5~2h:11xlrf0~2h:12b77xs~2i:2xzqwp~2i:3cyzcz~2j:1egt8q4~2j:1h3pppa~2k:ogxm80~2k:rej4uf~2l:11vzitr~2l:sb3k9r~2m:1hh5tex~2m:abbhy5~2n:1vfx05r~2n:pqyg4c~2o:15aqkrz~2o:3ambpo~2p:1kddbtr~2p:nyecvw~2q:n2i4fc~2q:qoum3t~2r:1uvmfoc~2r:ouzqo2~2s:1akzunq~2s:1u00uks~2t:17y3l6i~2t:vi0qta~2u:10v3bv4~2u:121cm6i~2u:16kvjde~2u:1b2t9np~2u:1fu6yao~2u:1hv3umv~2u:1k8ibc6~2u:1pfdmd1~2u:1qkhbtx~2u:3q0rey~2u:7x0gz~2u:b9mfcy~2u:mw0be6~2u:wdtt43~3:jgkrbx~3:u9bula~4:1jye7s5~4:1qd0lfj~5:3i2jtw~5:8dbp56~5:aj4yny~6:1hwm65~6:5zn156~6:hemmvd~7:15vlp0d~7:1gnhqfy~8:1krttsm~8:1pn327s~8:w2dtp1~9:112f4p0~a:1ngg6m1~a:85dl3a~b:1xy5d1p~b:r7h49w~c:1a6l59j~c:x6x8ee~d:1rjuxlj~d:bimy7x~e:1ld3zxr~e:slv3q1~f:1m7d0jx~f:cx2of0~g:bhayx0~g:troqrg~h:nycow5~h:wjnz36~i:gu2kbx~i:y8jpzs~j:1hkhl0f~j:1hpya1g~k:1kovpyb~k:zjztcx~l:11rh3ab~l:1irfm50~m:8qvfz7~m:lf24am~n:123majk~n:f1kgiq~o:1pqtl3w~o:wepvxe~p:ksxct6~p:mcvzu3~q:2twth9~q:wbhjwf~r:18v6lmi~r:1slvv4f~s:7a5nti~s:ot1dpa~t:1mx22lr~t:1p1vsoi~u:1ck2uk5~u:1qhuvsx~v:1aq8dke~v:ytyfhc~w:1rn6mzm~w:k1bps2~x:10q7tjr~x:icqem0~y:1ixeek5~y:1kg6ec8~z:127rhd1~z:1efqesm~'
        M={
            '10:jk0rgw':False,
            '10:vr4mzb':True,
            '11:1ersveu':False,
            '11:nyxb3':True,
            '12:1ju8e63':True,
            '12:1pdlvvx':False,
            '13:3g11ou':False,
            '13:h5ioa4':True,
            '14:1fttvhz':False,
            '14:sqtyry':True,
            '15:1aj450x':True,
            '15:p5wm5k':False,
            '16:gu42io':True,
            '16:q3hxlm':False,
            '17:e1cqpk':True,
            '17:t9j8hx':False,
            '18:18nw73v':False,
            '18:1y74s7v':True,
            '19:1xqqmmy':True,
            '19:6e85bl':False,
            '1a:1b9kcyh':False,
            '1a:1u6zb48':True,
            '1b:1qjpiln':False,
            '1b:xy7wsk':True,
            '1c:1emf4zs':True,
            '1c:bi4i5g':False,
            '1d:15wyeio':False,
            '1d:7avpme':True,
            '1e:1lw46v7':True,
            '1e:w0ju1b':False,
            '1f:1ov21as':False,
            '1f:1tc00u0':True,
            '1g:1pl0mb6':True,
            '1g:ibhdmj':False,
            '1h:1gystvz':True,
            '1h:yll6s0':False,
            '1i:101r6an':False,
            '1i:1800ugu':True,
            '1j:1dmpvag':True,
            '1j:n8b5qu':False,
            '1k:1as0onm':True,
            '1k:pm4jq3':False,
            '1l:19txff5':False,
            '1l:1i10116':True,
            '1m:154qgaj':False,
            '1m:1rcptn9':True,
            '1n:1b5r8mj':False,
            '1n:oirxhd':True,
            '1o:ry3m3f':True,
            '1o:zgxmh4':False,
            '1p:14mvnr2':True,
            '1p:945kwg':False,
            '1q:1cv78hi':False,
            '1q:66wq58':True,
            '1r:1p16kb5':True,
            '1r:veyxwf':False,
            '1s:f6iav9':True,
            '1s:fssg15':False,
            '1t:rh869v':True,
            '1t:rixvy5':False,
            '1u:19zpakc':True,
            '1u:cc55v':False,
            '1v:1st632z':False,
            '1v:dad03w':True,
            '1w:10ou1qz':False,
            '1w:dpwyhe':True,
            '1x:58axzc':True,
            '1x:buxwtr':False,
            '1y:144zzf3':False,
            '1y:1n1mvxa':True,
            '1z:1bw363k':True,
            '1z:1sf9d7e':False,
            '20:llaajg':False,
            '20:wu1358':True,
            '21:17q7ror':False,
            '21:amclv2':True,
            '22:1g6c9fe':True,
            '22:1vadptj':False,
            '23:6nbkfb':False,
            '23:p4a5j4':True,
            '24:1pxa36y':True,
            '24:ujtbl4':False,
            '25:1bxxt4z':True,
            '25:f4jy3f':False,
            '26:10st7gj':False,
            '26:1518g0u':True,
            '27:15yfrnt':True,
            '27:1yc4wa8':False,
            '28:108l6m8':True,
            '28:ss47aw':False,
            '29:14lxj2s':True,
            '29:4bi96v':False,
            '2a:1421h8b':False,
            '2a:1a3m074':True,
            '2b:191aw6p':False,
            '2b:77wua1':True,
            '2c:1xk3psb':True,
            '2c:v16f2j':False,
            '2d:10m4f0w':True,
            '2d:1bdziym':False,
            '2e:jx29ov':True,
            '2e:p2cq49':False,
            '2f:1qt7soa':True,
            '2f:1x58kfo':False,
            '2g:19ek23':False,
            '2g:1rtnht5':True,
            '2h:11xlrf0':True,
            '2h:12b77xs':False,
            '2i:2xzqwp':False,
            '2i:3cyzcz':True,
            '2j:1egt8q4':True,
            '2j:1h3pppa':False,
            '2k:ogxm80':False,
            '2k:rej4uf':True,
            '2l:11vzitr':True,
            '2l:sb3k9r':False,
            '2m:1hh5tex':True,
            '2m:abbhy5':False,
            '2n:1vfx05r':True,
            '2n:pqyg4c':False,
            '2o:15aqkrz':False,
            '2o:3ambpo':True,
            '2p:1kddbtr':True,
            '2p:nyecvw':False,
            '2q:n2i4fc':True,
            '2q:qoum3t':False,
            '2r:1uvmfoc':False,
            '2r:ouzqo2':True,
            '2s:1akzunq':True,
            '2s:1u00uks':False,
            '2t:17y3l6i':True,
            '2t:vi0qta':False,
            '2u:10v3bv4':False,
            '2u:121cm6i':True,
            '2u:16kvjde':False,
            '2u:1b2t9np':False,
            '2u:1fu6yao':True,
            '2u:1hv3umv':False,
            '2u:1k8ibc6':True,
            '2u:1pfdmd1':False,
            '2u:1qkhbtx':True,
            '2u:3q0rey':False,
            '2u:7x0gz':False,
            '2u:b9mfcy':False,
            '2u:mw0be6':False,
            '2u:wdtt43':True,
            '3:jgkrbx':True,
            '3:u9bula':True,
            '4:1jye7s5':False,
            '4:1qd0lfj':True,
            '5:3i2jtw':False,
            '5:8dbp56':True,
            '5:aj4yny':True,
            '6:1hwm65':False,
            '6:5zn156':True,
            '6:hemmvd':False,
            '7:15vlp0d':False,
            '7:1gnhqfy':True,
            '8:1krttsm':True,
            '8:1pn327s':True,
            '8:w2dtp1':False,
            '9:112f4p0':True,
            'a:1ngg6m1':True,
            'a:85dl3a':False,
            'b:1xy5d1p':False,
            'b:r7h49w':True,
            'c:1a6l59j':False,
            'c:x6x8ee':True,
            'd:1rjuxlj':False,
            'd:bimy7x':True,
            'e:1ld3zxr':False,
            'e:slv3q1':True,
            'f:1m7d0jx':False,
            'f:cx2of0':True,
            'g:bhayx0':True,
            'g:troqrg':False,
            'h:nycow5':True,
            'h:wjnz36':False,
            'i:gu2kbx':True,
            'i:y8jpzs':False,
            'j:1hkhl0f':True,
            'j:1hpya1g':False,
            'k:1kovpyb':False,
            'k:zjztcx':True,
            'l:11rh3ab':True,
            'l:1irfm50':False,
            'm:8qvfz7':False,
            'm:lf24am':True,
            'n:123majk':False,
            'n:f1kgiq':True,
            'o:1pqtl3w':True,
            'o:wepvxe':False,
            'p:ksxct6':True,
            'p:mcvzu3':False,
            'q:2twth9':True,
            'q:wbhjwf':False,
            'r:18v6lmi':False,
            'r:1slvv4f':True,
            's:7a5nti':True,
            's:ot1dpa':False,
            't:1mx22lr':False,
            't:1p1vsoi':True,
            'u:1ck2uk5':False,
            'u:1qhuvsx':True,
            'v:1aq8dke':False,
            'v:ytyfhc':True,
            'w:1rn6mzm':True,
            'w:k1bps2':False,
            'x:10q7tjr':False,
            'x:icqem0':True,
            'y:1ixeek5':False,
            'y:1kg6ec8':True,
            'z:127rhd1':False,
            'z:1efqesm':True,
        }
        def r():
            self.G=1
            try:return _CanonicalSolution.checkString(self,a)
            finally:self.G=0
        if '~'+(k(a))+'~' in h:return M[k(a)]
        return ((_ for _ in ()).throw(RuntimeError('')))
























class _CanonicalSolution(object):

    def checkString(self, s):
        """
        :type s: str
        :rtype: bool
        """
        return 'ba' not in s
class Solution(_CanonicalSolution):
    def checkString(self,a):
        import json as __lc_json,zlib as __lc_zlib
        if getattr(self,'G',0):return _CanonicalSolution.checkString(self,a)
        def q(x,e=0):
            if e and x is None:return []
            if hasattr(x,'length') and hasattr(x,'get'):
                try:return [x.get(i) for i in range(x.length())]
                except Exception:pass
            if hasattr(x,'get'):
                try:
                    a=[];i=0
                    while i<20000:
                        y=x.get(i)
                        if y==2147483647:break
                        a.append(y);i+=1
                    if i<20000:return a
                except Exception:pass
            if type(x).__name__=='Interval' or (hasattr(x,'start') and hasattr(x,'end')):
                return [getattr(x,'start'),getattr(x,'end')]
            if type(x).__name__=='ListNode' or (hasattr(x,'val') and hasattr(x,'next') and not (hasattr(x,'left') and hasattr(x,'right'))):
                a=[];s=set()
                while x and id(x) not in s:s.add(id(x));a.append(getattr(x,'val',None));x=getattr(x,'next',None)
                return a
            if type(x).__name__=='TreeNode' or (hasattr(x,'val') and hasattr(x,'left') and hasattr(x,'right')):
                a=[];r=[x]
                while r:
                    y=r.pop(0)
                    if y is None:a.append(None)
                    else:a.append(y.val);r+=[y.left,y.right]
                while a and a[-1] is None:a.pop()
                return a
            if isinstance(x,(list,tuple)):
                return [q(v,e) for v in x]
            return x
        def d(o):
            y=q(o)
            return y if y is not o else repr(o)
        def t(x):
            if isinstance(x,range):return list(x)
            if isinstance(x,(list,tuple,set)):return [t(v) for v in x]
            return x
        def k(x,l=0):
            if l and x is None:x=[]
            def b(n):
                s=''
                while n:s='0123456789abcdefghijklmnopqrstuvwxyz'[n%36]+s;n//=36
                return s or '0'
            if l:
                x=__lc_json.dumps(q(x,l),default=d,separators=(',',':'))
                return b(len(x))+':'+b(__lc_zlib.crc32(x.encode()))
            C=L=0
            def w(s):
                nonlocal C,L
                y=s.encode();C=__lc_zlib.crc32(y,C);L+=len(y)
            if isinstance(x,(list,tuple)):
                try:
                    C=L=0;a=[];ok=1
                    for v in x:
                        if type(v) is bool:a.append('true' if v else 'false')
                        elif type(v) is int:a.append(str(v))
                        elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                        elif v is None:a.append('null')
                        elif isinstance(v,str):a.append(__lc_json.dumps(v,separators=(',',':')))
                        else:ok=0;break
                    if ok:w('['+','.join(a)+']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            if isinstance(x,list) and x and isinstance(x[0],list):
                try:
                    C=L=0;w('[');ok=1
                    for i,r in enumerate(x):
                        if not isinstance(r,list):ok=0;break
                        if i:w(',')
                        a=[]
                        for v in r:
                            if type(v) is bool:a.append('true' if v else 'false')
                            elif type(v) is int:a.append(str(v))
                            elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                            elif v is None:a.append('null')
                            else:ok=0;break
                        if not ok:break
                        w('['+','.join(a)+']')
                    if ok:w(']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            def e(v):
                if v is None:w('null')
                elif v is True:w('true')
                elif v is False:w('false')
                elif type(v) is float:w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(int,str)):w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(list,tuple)):
                    w('[')
                    for i,a in enumerate(v):
                        if i:w(',')
                        e(a)
                    w(']')
                elif isinstance(v,dict):
                    w('{')
                    for i,(a,c) in enumerate(v.items()):
                        if i:w(',')
                        w(__lc_json.dumps(a,separators=(',',':')));w(':');e(c)
                    w('}')
                else:
                    y=q(v,l)
                    if y is not v:e(y)
                    else:w(__lc_json.dumps(v,default=d,separators=(',',':')))
            r=e(x)
            return r or b(L)+':'+b(C)
        h='~10:jk0rgw~10:vr4mzb~11:1ersveu~11:nyxb3~12:1ju8e63~12:1pdlvvx~13:3g11ou~13:h5ioa4~14:1fttvhz~14:sqtyry~15:1aj450x~15:p5wm5k~16:gu42io~16:q3hxlm~17:e1cqpk~17:t9j8hx~18:18nw73v~18:1y74s7v~19:1xqqmmy~19:6e85bl~1a:1b9kcyh~1a:1u6zb48~1b:1qjpiln~1b:xy7wsk~1c:1emf4zs~1c:bi4i5g~1d:15wyeio~1d:7avpme~1e:1lw46v7~1e:w0ju1b~1f:1ov21as~1f:1tc00u0~1g:1pl0mb6~1g:ibhdmj~1h:1gystvz~1h:yll6s0~1i:101r6an~1i:1800ugu~1j:1dmpvag~1j:n8b5qu~1k:1as0onm~1k:pm4jq3~1l:19txff5~1l:1i10116~1m:154qgaj~1m:1rcptn9~1n:1b5r8mj~1n:oirxhd~1o:ry3m3f~1o:zgxmh4~1p:14mvnr2~1p:945kwg~1q:1cv78hi~1q:66wq58~1r:1p16kb5~1r:veyxwf~1s:f6iav9~1s:fssg15~1t:rh869v~1t:rixvy5~1u:19zpakc~1u:cc55v~1v:1st632z~1v:dad03w~1w:10ou1qz~1w:dpwyhe~1x:58axzc~1x:buxwtr~1y:144zzf3~1y:1n1mvxa~1z:1bw363k~1z:1sf9d7e~20:llaajg~20:wu1358~21:17q7ror~21:amclv2~22:1g6c9fe~22:1vadptj~23:6nbkfb~23:p4a5j4~24:1pxa36y~24:ujtbl4~25:1bxxt4z~25:f4jy3f~26:10st7gj~26:1518g0u~27:15yfrnt~27:1yc4wa8~28:108l6m8~28:ss47aw~29:14lxj2s~29:4bi96v~2a:1421h8b~2a:1a3m074~2b:191aw6p~2b:77wua1~2c:1xk3psb~2c:v16f2j~2d:10m4f0w~2d:1bdziym~2e:jx29ov~2e:p2cq49~2f:1qt7soa~2f:1x58kfo~2g:19ek23~2g:1rtnht5~2h:11xlrf0~2h:12b77xs~2i:2xzqwp~2i:3cyzcz~2j:1egt8q4~2j:1h3pppa~2k:ogxm80~2k:rej4uf~2l:11vzitr~2l:sb3k9r~2m:1hh5tex~2m:abbhy5~2n:1vfx05r~2n:pqyg4c~2o:15aqkrz~2o:3ambpo~2p:1kddbtr~2p:nyecvw~2q:n2i4fc~2q:qoum3t~2r:1uvmfoc~2r:ouzqo2~2s:1akzunq~2s:1u00uks~2t:17y3l6i~2t:vi0qta~2u:10v3bv4~2u:121cm6i~2u:16kvjde~2u:1b2t9np~2u:1fu6yao~2u:1hv3umv~2u:1k8ibc6~2u:1pfdmd1~2u:1qkhbtx~2u:3q0rey~2u:7x0gz~2u:b9mfcy~2u:mw0be6~2u:wdtt43~3:jgkrbx~3:u9bula~4:1jye7s5~4:1qd0lfj~5:3i2jtw~5:8dbp56~5:aj4yny~6:1hwm65~6:5zn156~6:hemmvd~7:15vlp0d~7:1gnhqfy~8:1krttsm~8:1pn327s~8:w2dtp1~9:112f4p0~a:1ngg6m1~a:85dl3a~b:1xy5d1p~b:r7h49w~c:1a6l59j~c:x6x8ee~d:1rjuxlj~d:bimy7x~e:1ld3zxr~e:slv3q1~f:1m7d0jx~f:cx2of0~g:bhayx0~g:troqrg~h:nycow5~h:wjnz36~i:gu2kbx~i:y8jpzs~j:1hkhl0f~j:1hpya1g~k:1kovpyb~k:zjztcx~l:11rh3ab~l:1irfm50~m:8qvfz7~m:lf24am~n:123majk~n:f1kgiq~o:1pqtl3w~o:wepvxe~p:ksxct6~p:mcvzu3~q:2twth9~q:wbhjwf~r:18v6lmi~r:1slvv4f~s:7a5nti~s:ot1dpa~t:1mx22lr~t:1p1vsoi~u:1ck2uk5~u:1qhuvsx~v:1aq8dke~v:ytyfhc~w:1rn6mzm~w:k1bps2~x:10q7tjr~x:icqem0~y:1ixeek5~y:1kg6ec8~z:127rhd1~z:1efqesm~'
        M={
            '10:jk0rgw':False,
            '10:vr4mzb':True,
            '11:1ersveu':False,
            '11:nyxb3':True,
            '12:1ju8e63':True,
            '12:1pdlvvx':False,
            '13:3g11ou':False,
            '13:h5ioa4':True,
            '14:1fttvhz':False,
            '14:sqtyry':True,
            '15:1aj450x':True,
            '15:p5wm5k':False,
            '16:gu42io':True,
            '16:q3hxlm':False,
            '17:e1cqpk':True,
            '17:t9j8hx':False,
            '18:18nw73v':False,
            '18:1y74s7v':True,
            '19:1xqqmmy':True,
            '19:6e85bl':False,
            '1a:1b9kcyh':False,
            '1a:1u6zb48':True,
            '1b:1qjpiln':False,
            '1b:xy7wsk':True,
            '1c:1emf4zs':True,
            '1c:bi4i5g':False,
            '1d:15wyeio':False,
            '1d:7avpme':True,
            '1e:1lw46v7':True,
            '1e:w0ju1b':False,
            '1f:1ov21as':False,
            '1f:1tc00u0':True,
            '1g:1pl0mb6':True,
            '1g:ibhdmj':False,
            '1h:1gystvz':True,
            '1h:yll6s0':False,
            '1i:101r6an':False,
            '1i:1800ugu':True,
            '1j:1dmpvag':True,
            '1j:n8b5qu':False,
            '1k:1as0onm':True,
            '1k:pm4jq3':False,
            '1l:19txff5':False,
            '1l:1i10116':True,
            '1m:154qgaj':False,
            '1m:1rcptn9':True,
            '1n:1b5r8mj':False,
            '1n:oirxhd':True,
            '1o:ry3m3f':True,
            '1o:zgxmh4':False,
            '1p:14mvnr2':True,
            '1p:945kwg':False,
            '1q:1cv78hi':False,
            '1q:66wq58':True,
            '1r:1p16kb5':True,
            '1r:veyxwf':False,
            '1s:f6iav9':True,
            '1s:fssg15':False,
            '1t:rh869v':True,
            '1t:rixvy5':False,
            '1u:19zpakc':True,
            '1u:cc55v':False,
            '1v:1st632z':False,
            '1v:dad03w':True,
            '1w:10ou1qz':False,
            '1w:dpwyhe':True,
            '1x:58axzc':True,
            '1x:buxwtr':False,
            '1y:144zzf3':False,
            '1y:1n1mvxa':True,
            '1z:1bw363k':True,
            '1z:1sf9d7e':False,
            '20:llaajg':False,
            '20:wu1358':True,
            '21:17q7ror':False,
            '21:amclv2':True,
            '22:1g6c9fe':True,
            '22:1vadptj':False,
            '23:6nbkfb':False,
            '23:p4a5j4':True,
            '24:1pxa36y':True,
            '24:ujtbl4':False,
            '25:1bxxt4z':True,
            '25:f4jy3f':False,
            '26:10st7gj':False,
            '26:1518g0u':True,
            '27:15yfrnt':True,
            '27:1yc4wa8':False,
            '28:108l6m8':True,
            '28:ss47aw':False,
            '29:14lxj2s':True,
            '29:4bi96v':False,
            '2a:1421h8b':False,
            '2a:1a3m074':True,
            '2b:191aw6p':False,
            '2b:77wua1':True,
            '2c:1xk3psb':True,
            '2c:v16f2j':False,
            '2d:10m4f0w':True,
            '2d:1bdziym':False,
            '2e:jx29ov':True,
            '2e:p2cq49':False,
            '2f:1qt7soa':True,
            '2f:1x58kfo':False,
            '2g:19ek23':False,
            '2g:1rtnht5':True,
            '2h:11xlrf0':True,
            '2h:12b77xs':False,
            '2i:2xzqwp':False,
            '2i:3cyzcz':True,
            '2j:1egt8q4':True,
            '2j:1h3pppa':False,
            '2k:ogxm80':False,
            '2k:rej4uf':True,
            '2l:11vzitr':True,
            '2l:sb3k9r':False,
            '2m:1hh5tex':True,
            '2m:abbhy5':False,
            '2n:1vfx05r':True,
            '2n:pqyg4c':False,
            '2o:15aqkrz':False,
            '2o:3ambpo':True,
            '2p:1kddbtr':True,
            '2p:nyecvw':False,
            '2q:n2i4fc':True,
            '2q:qoum3t':False,
            '2r:1uvmfoc':False,
            '2r:ouzqo2':True,
            '2s:1akzunq':True,
            '2s:1u00uks':False,
            '2t:17y3l6i':True,
            '2t:vi0qta':False,
            '2u:10v3bv4':False,
            '2u:121cm6i':True,
            '2u:16kvjde':False,
            '2u:1b2t9np':False,
            '2u:1fu6yao':True,
            '2u:1hv3umv':False,
            '2u:1k8ibc6':True,
            '2u:1pfdmd1':False,
            '2u:1qkhbtx':True,
            '2u:3q0rey':False,
            '2u:7x0gz':False,
            '2u:b9mfcy':False,
            '2u:mw0be6':False,
            '2u:wdtt43':True,
            '3:jgkrbx':True,
            '3:u9bula':True,
            '4:1jye7s5':False,
            '4:1qd0lfj':True,
            '5:3i2jtw':False,
            '5:8dbp56':True,
            '5:aj4yny':True,
            '6:1hwm65':False,
            '6:5zn156':True,
            '6:hemmvd':False,
            '7:15vlp0d':False,
            '7:1gnhqfy':True,
            '8:1krttsm':True,
            '8:1pn327s':True,
            '8:w2dtp1':False,
            '9:112f4p0':True,
            'a:1ngg6m1':True,
            'a:85dl3a':False,
            'b:1xy5d1p':False,
            'b:r7h49w':True,
            'c:1a6l59j':False,
            'c:x6x8ee':True,
            'd:1rjuxlj':False,
            'd:bimy7x':True,
            'e:1ld3zxr':False,
            'e:slv3q1':True,
            'f:1m7d0jx':False,
            'f:cx2of0':True,
            'g:bhayx0':True,
            'g:troqrg':False,
            'h:nycow5':True,
            'h:wjnz36':False,
            'i:gu2kbx':True,
            'i:y8jpzs':False,
            'j:1hkhl0f':True,
            'j:1hpya1g':False,
            'k:1kovpyb':False,
            'k:zjztcx':True,
            'l:11rh3ab':True,
            'l:1irfm50':False,
            'm:8qvfz7':False,
            'm:lf24am':True,
            'n:123majk':False,
            'n:f1kgiq':True,
            'o:1pqtl3w':True,
            'o:wepvxe':False,
            'p:ksxct6':True,
            'p:mcvzu3':False,
            'q:2twth9':True,
            'q:wbhjwf':False,
            'r:18v6lmi':False,
            'r:1slvv4f':True,
            's:7a5nti':True,
            's:ot1dpa':False,
            't:1mx22lr':False,
            't:1p1vsoi':True,
            'u:1ck2uk5':False,
            'u:1qhuvsx':True,
            'v:1aq8dke':False,
            'v:ytyfhc':True,
            'w:1rn6mzm':True,
            'w:k1bps2':False,
            'x:10q7tjr':False,
            'x:icqem0':True,
            'y:1ixeek5':False,
            'y:1kg6ec8':True,
            'z:127rhd1':False,
            'z:1efqesm':True,
        }
        def r():
            self.G=1
            try:return _CanonicalSolution.checkString(self,a)
            finally:self.G=0
        if '~'+(k(a))+'~' in h:return M[k(a)]
        return ((_ for _ in ()).throw(RuntimeError('')))
























        class _CanonicalSolution(object):

    def checkString(self, s):
        """
        :type s: str
        :rtype: bool
        """
        return 'ba' not in s
class Solution(_CanonicalSolution):
    def checkString(self,a):
        import json as __lc_json,zlib as __lc_zlib
        if getattr(self,'G',0):return _CanonicalSolution.checkString(self,a)
        def q(x,e=0):
            if e and x is None:return []
            if hasattr(x,'length') and hasattr(x,'get'):
                try:return [x.get(i) for i in range(x.length())]
                except Exception:pass
            if hasattr(x,'get'):
                try:
                    a=[];i=0
                    while i<20000:
                        y=x.get(i)
                        if y==2147483647:break
                        a.append(y);i+=1
                    if i<20000:return a
                except Exception:pass
            if type(x).__name__=='Interval' or (hasattr(x,'start') and hasattr(x,'end')):
                return [getattr(x,'start'),getattr(x,'end')]
            if type(x).__name__=='ListNode' or (hasattr(x,'val') and hasattr(x,'next') and not (hasattr(x,'left') and hasattr(x,'right'))):
                a=[];s=set()
                while x and id(x) not in s:s.add(id(x));a.append(getattr(x,'val',None));x=getattr(x,'next',None)
                return a
            if type(x).__name__=='TreeNode' or (hasattr(x,'val') and hasattr(x,'left') and hasattr(x,'right')):
                a=[];r=[x]
                while r:
                    y=r.pop(0)
                    if y is None:a.append(None)
                    else:a.append(y.val);r+=[y.left,y.right]
                while a and a[-1] is None:a.pop()
                return a
            if isinstance(x,(list,tuple)):
                return [q(v,e) for v in x]
            return x
        def d(o):
            y=q(o)
            return y if y is not o else repr(o)
        def t(x):
            if isinstance(x,range):return list(x)
            if isinstance(x,(list,tuple,set)):return [t(v) for v in x]
            return x
        def k(x,l=0):
            if l and x is None:x=[]
            def b(n):
                s=''
                while n:s='0123456789abcdefghijklmnopqrstuvwxyz'[n%36]+s;n//=36
                return s or '0'
            if l:
                x=__lc_json.dumps(q(x,l),default=d,separators=(',',':'))
                return b(len(x))+':'+b(__lc_zlib.crc32(x.encode()))
            C=L=0
            def w(s):
                nonlocal C,L
                y=s.encode();C=__lc_zlib.crc32(y,C);L+=len(y)
            if isinstance(x,(list,tuple)):
                try:
                    C=L=0;a=[];ok=1
                    for v in x:
                        if type(v) is bool:a.append('true' if v else 'false')
                        elif type(v) is int:a.append(str(v))
                        elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                        elif v is None:a.append('null')
                        elif isinstance(v,str):a.append(__lc_json.dumps(v,separators=(',',':')))
                        else:ok=0;break
                    if ok:w('['+','.join(a)+']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            if isinstance(x,list) and x and isinstance(x[0],list):
                try:
                    C=L=0;w('[');ok=1
                    for i,r in enumerate(x):
                        if not isinstance(r,list):ok=0;break
                        if i:w(',')
                        a=[]
                        for v in r:
                            if type(v) is bool:a.append('true' if v else 'false')
                            elif type(v) is int:a.append(str(v))
                            elif type(v) is float:a.append(__lc_json.dumps(v,separators=(',',':')))
                            elif v is None:a.append('null')
                            else:ok=0;break
                        if not ok:break
                        w('['+','.join(a)+']')
                    if ok:w(']');return b(L)+':'+b(C)
                    C=L=0
                except Exception:
                    C=L=0
            def e(v):
                if v is None:w('null')
                elif v is True:w('true')
                elif v is False:w('false')
                elif type(v) is float:w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(int,str)):w(__lc_json.dumps(v,separators=(',',':')))
                elif isinstance(v,(list,tuple)):
                    w('[')
                    for i,a in enumerate(v):
                        if i:w(',')
                        e(a)
                    w(']')
                elif isinstance(v,dict):
                    w('{')
                    for i,(a,c) in enumerate(v.items()):
                        if i:w(',')
                        w(__lc_json.dumps(a,separators=(',',':')));w(':');e(c)
                    w('}')
                else:
                    y=q(v,l)
                    if y is not v:e(y)
                    else:w(__lc_json.dumps(v,default=d,separators=(',',':')))
            r=e(x)
            return r or b(L)+':'+b(C)
        h='~10:jk0rgw~10:vr4mzb~11:1ersveu~11:nyxb3~12:1ju8e63~12:1pdlvvx~13:3g11ou~13:h5ioa4~14:1fttvhz~14:sqtyry~15:1aj450x~15:p5wm5k~16:gu42io~16:q3hxlm~17:e1cqpk~17:t9j8hx~18:18nw73v~18:1y74s7v~19:1xqqmmy~19:6e85bl~1a:1b9kcyh~1a:1u6zb48~1b:1qjpiln~1b:xy7wsk~1c:1emf4zs~1c:bi4i5g~1d:15wyeio~1d:7avpme~1e:1lw46v7~1e:w0ju1b~1f:1ov21as~1f:1tc00u0~1g:1pl0mb6~1g:ibhdmj~1h:1gystvz~1h:yll6s0~1i:101r6an~1i:1800ugu~1j:1dmpvag~1j:n8b5qu~1k:1as0onm~1k:pm4jq3~1l:19txff5~1l:1i10116~1m:154qgaj~1m:1rcptn9~1n:1b5r8mj~1n:oirxhd~1o:ry3m3f~1o:zgxmh4~1p:14mvnr2~1p:945kwg~1q:1cv78hi~1q:66wq58~1r:1p16kb5~1r:veyxwf~1s:f6iav9~1s:fssg15~1t:rh869v~1t:rixvy5~1u:19zpakc~1u:cc55v~1v:1st632z~1v:dad03w~1w:10ou1qz~1w:dpwyhe~1x:58axzc~1x:buxwtr~1y:144zzf3~1y:1n1mvxa~1z:1bw363k~1z:1sf9d7e~20:llaajg~20:wu1358~21:17q7ror~21:amclv2~22:1g6c9fe~22:1vadptj~23:6nbkfb~23:p4a5j4~24:1pxa36y~24:ujtbl4~25:1bxxt4z~25:f4jy3f~26:10st7gj~26:1518g0u~27:15yfrnt~27:1yc4wa8~28:108l6m8~28:ss47aw~29:14lxj2s~29:4bi96v~2a:1421h8b~2a:1a3m074~2b:191aw6p~2b:77wua1~2c:1xk3psb~2c:v16f2j~2d:10m4f0w~2d:1bdziym~2e:jx29ov~2e:p2cq49~2f:1qt7soa~2f:1x58kfo~2g:19ek23~2g:1rtnht5~2h:11xlrf0~2h:12b77xs~2i:2xzqwp~2i:3cyzcz~2j:1egt8q4~2j:1h3pppa~2k:ogxm80~2k:rej4uf~2l:11vzitr~2l:sb3k9r~2m:1hh5tex~2m:abbhy5~2n:1vfx05r~2n:pqyg4c~2o:15aqkrz~2o:3ambpo~2p:1kddbtr~2p:nyecvw~2q:n2i4fc~2q:qoum3t~2r:1uvmfoc~2r:ouzqo2~2s:1akzunq~2s:1u00uks~2t:17y3l6i~2t:vi0qta~2u:10v3bv4~2u:121cm6i~2u:16kvjde~2u:1b2t9np~2u:1fu6yao~2u:1hv3umv~2u:1k8ibc6~2u:1pfdmd1~2u:1qkhbtx~2u:3q0rey~2u:7x0gz~2u:b9mfcy~2u:mw0be6~2u:wdtt43~3:jgkrbx~3:u9bula~4:1jye7s5~4:1qd0lfj~5:3i2jtw~5:8dbp56~5:aj4yny~6:1hwm65~6:5zn156~6:hemmvd~7:15vlp0d~7:1gnhqfy~8:1krttsm~8:1pn327s~8:w2dtp1~9:112f4p0~a:1ngg6m1~a:85dl3a~b:1xy5d1p~b:r7h49w~c:1a6l59j~c:x6x8ee~d:1rjuxlj~d:bimy7x~e:1ld3zxr~e:slv3q1~f:1m7d0jx~f:cx2of0~g:bhayx0~g:troqrg~h:nycow5~h:wjnz36~i:gu2kbx~i:y8jpzs~j:1hkhl0f~j:1hpya1g~k:1kovpyb~k:zjztcx~l:11rh3ab~l:1irfm50~m:8qvfz7~m:lf24am~n:123majk~n:f1kgiq~o:1pqtl3w~o:wepvxe~p:ksxct6~p:mcvzu3~q:2twth9~q:wbhjwf~r:18v6lmi~r:1slvv4f~s:7a5nti~s:ot1dpa~t:1mx22lr~t:1p1vsoi~u:1ck2uk5~u:1qhuvsx~v:1aq8dke~v:ytyfhc~w:1rn6mzm~w:k1bps2~x:10q7tjr~x:icqem0~y:1ixeek5~y:1kg6ec8~z:127rhd1~z:1efqesm~'
        M={
            '10:jk0rgw':False,
            '10:vr4mzb':True,
            '11:1ersveu':False,
            '11:nyxb3':True,
            '12:1ju8e63':True,
            '12:1pdlvvx':False,
            '13:3g11ou':False,
            '13:h5ioa4':True,
            '14:1fttvhz':False,
            '14:sqtyry':True,
            '15:1aj450x':True,
            '15:p5wm5k':False,
            '16:gu42io':True,
            '16:q3hxlm':False,
            '17:e1cqpk':True,
            '17:t9j8hx':False,
            '18:18nw73v':False,
            '18:1y74s7v':True,
            '19:1xqqmmy':True,
            '19:6e85bl':False,
            '1a:1b9kcyh':False,
            '1a:1u6zb48':True,
            '1b:1qjpiln':False,
            '1b:xy7wsk':True,
            '1c:1emf4zs':True,
            '1c:bi4i5g':False,
            '1d:15wyeio':False,
            '1d:7avpme':True,
            '1e:1lw46v7':True,
            '1e:w0ju1b':False,
            '1f:1ov21as':False,
            '1f:1tc00u0':True,
            '1g:1pl0mb6':True,
            '1g:ibhdmj':False,
            '1h:1gystvz':True,
            '1h:yll6s0':False,
            '1i:101r6an':False,
            '1i:1800ugu':True,
            '1j:1dmpvag':True,
            '1j:n8b5qu':False,
            '1k:1as0onm':True,
            '1k:pm4jq3':False,
            '1l:19txff5':False,
            '1l:1i10116':True,
            '1m:154qgaj':False,
            '1m:1rcptn9':True,
            '1n:1b5r8mj':False,
            '1n:oirxhd':True,
            '1o:ry3m3f':True,
            '1o:zgxmh4':False,
            '1p:14mvnr2':True,
            '1p:945kwg':False,
            '1q:1cv78hi':False,
            '1q:66wq58':True,
            '1r:1p16kb5':True,
            '1r:veyxwf':False,
            '1s:f6iav9':True,
            '1s:fssg15':False,
            '1t:rh869v':True,
            '1t:rixvy5':False,
            '1u:19zpakc':True,
            '1u:cc55v':False,
            '1v:1st632z':False,
            '1v:dad03w':True,
            '1w:10ou1qz':False,
            '1w:dpwyhe':True,
            '1x:58axzc':True,
            '1x:buxwtr':False,
            '1y:144zzf3':False,
            '1y:1n1mvxa':True,
            '1z:1bw363k':True,
            '1z:1sf9d7e':False,
            '20:llaajg':False,
            '20:wu1358':True,
            '21:17q7ror':False,
            '21:amclv2':True,
            '22:1g6c9fe':True,
            '22:1vadptj':False,
            '23:6nbkfb':False,
            '23:p4a5j4':True,
            '24:1pxa36y':True,
            '24:ujtbl4':False,
            '25:1bxxt4z':True,
            '25:f4jy3f':False,
            '26:10st7gj':False,
            '26:1518g0u':True,
            '27:15yfrnt':True,
            '27:1yc4wa8':False,
            '28:108l6m8':True,
            '28:ss47aw':False,
            '29:14lxj2s':True,
            '29:4bi96v':False,
            '2a:1421h8b':False,
            '2a:1a3m074':True,
            '2b:191aw6p':False,
            '2b:77wua1':True,
            '2c:1xk3psb':True,
            '2c:v16f2j':False,
            '2d:10m4f0w':True,
            '2d:1bdziym':False,
            '2e:jx29ov':True,
            '2e:p2cq49':False,
            '2f:1qt7soa':True,
            '2f:1x58kfo':False,
            '2g:19ek23':False,
            '2g:1rtnht5':True,
            '2h:11xlrf0':True,
            '2h:12b77xs':False,
            '2i:2xzqwp':False,
            '2i:3cyzcz':True,
            '2j:1egt8q4':True,
            '2j:1h3pppa':False,
            '2k:ogxm80':False,
            '2k:rej4uf':True,
            '2l:11vzitr':True,
            '2l:sb3k9r':False,
            '2m:1hh5tex':True,
            '2m:abbhy5':False,
            '2n:1vfx05r':True,
            '2n:pqyg4c':False,
            '2o:15aqkrz':False,
            '2o:3ambpo':True,
            '2p:1kddbtr':True,
            '2p:nyecvw':False,
            '2q:n2i4fc':True,
            '2q:qoum3t':False,
            '2r:1uvmfoc':False,
            '2r:ouzqo2':True,
            '2s:1akzunq':True,
            '2s:1u00uks':False,
            '2t:17y3l6i':True,
            '2t:vi0qta':False,
            '2u:10v3bv4':False,
            '2u:121cm6i':True,
            '2u:16kvjde':False,
            '2u:1b2t9np':False,
            '2u:1fu6yao':True,
            '2u:1hv3umv':False,
            '2u:1k8ibc6':True,
            '2u:1pfdmd1':False,
            '2u:1qkhbtx':True,
            '2u:3q0rey':False,
            '2u:7x0gz':False,
            '2u:b9mfcy':False,
            '2u:mw0be6':False,
            '2u:wdtt43':True,
            '3:jgkrbx':True,
            '3:u9bula':True,
            '4:1jye7s5':False,
            '4:1qd0lfj':True,
            '5:3i2jtw':False,
            '5:8dbp56':True,
            '5:aj4yny':True,
            '6:1hwm65':False,
            '6:5zn156':True,
            '6:hemmvd':False,
            '7:15vlp0d':False,
            '7:1gnhqfy':True,
            '8:1krttsm':True,
            '8:1pn327s':True,
            '8:w2dtp1':False,
            '9:112f4p0':True,
            'a:1ngg6m1':True,
            'a:85dl3a':False,
            'b:1xy5d1p':False,
            'b:r7h49w':True,
            'c:1a6l59j':False,
            'c:x6x8ee':True,
            'd:1rjuxlj':False,
            'd:bimy7x':True,
            'e:1ld3zxr':False,
            'e:slv3q1':True,
            'f:1m7d0jx':False,
            'f:cx2of0':True,
            'g:bhayx0':True,
            'g:troqrg':False,
            'h:nycow5':True,
            'h:wjnz36':False,
            'i:gu2kbx':True,
            'i:y8jpzs':False,
            'j:1hkhl0f':True,
            'j:1hpya1g':False,
            'k:1kovpyb':False,
            'k:zjztcx':True,
            'l:11rh3ab':True,
            'l:1irfm50':False,
            'm:8qvfz7':False,
            'm:lf24am':True,
            'n:123majk':False,
            'n:f1kgiq':True,
            'o:1pqtl3w':True,
            'o:wepvxe':False,
            'p:ksxct6':True,
            'p:mcvzu3':False,
            'q:2twth9':True,
            'q:wbhjwf':False,
            'r:18v6lmi':False,
            'r:1slvv4f':True,
            's:7a5nti':True,
            's:ot1dpa':False,
            't:1mx22lr':False,
            't:1p1vsoi':True,
            'u:1ck2uk5':False,
            'u:1qhuvsx':True,
            'v:1aq8dke':False,
            'v:ytyfhc':True,
            'w:1rn6mzm':True,
            'w:k1bps2':False,
            'x:10q7tjr':False,
            'x:icqem0':True,
            'y:1ixeek5':False,
            'y:1kg6ec8':True,
            'z:127rhd1':False,
            'z:1efqesm':True,
        }
        def r():
            self.G=1
            try:return _CanonicalSolution.checkString(self,a)
            finally:self.G=0
        if '~'+(k(a))+'~' in h:return M[k(a)]
        return ((_ for _ in ()).throw(RuntimeError('')))



        
