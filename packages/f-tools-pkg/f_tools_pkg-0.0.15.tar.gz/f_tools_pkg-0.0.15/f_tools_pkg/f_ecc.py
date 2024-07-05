class point:
    def __init__(self):
        self.x =""
        self.y =""
        self.z =""

class ecc_para:
    def __init__(self):
        self.p = ""
        self.a = ""
        self.b = ""
        self.g = point()
        self.n = ""
        
        self.pubkey=point()
        self.prikey=""
class NN_2m:
    def __init__(self):
        self.para = ecc_para()
    
    def s2n(self,v):
        return int(v,16) 
        
    def n2s(self,n):
        return hex(n).replace("0x","")
    
    def modmult(self,a,b,p):
        n_a = 0
        lenp = self.s2n(p).bit_length() - 1
        va = self.s2n(a)
        vb = self.s2n(b)
        vp = self.s2n(p)
        while vb:
            if vb & 1:
                n_a = n_a ^ va
            va = va << 1
            vb = vb >> 1
            if va >> lenp:
                va =va ^ vp
        return self.n2s(n_a)
    
    def div(self,b,c):
        result=[]
        vq = 0
        vb = self.s2n(b) 
        vc = self.s2n(c)
        lenb = vb.bit_length()
        lenc = vc.bit_length()
        while not vb < vc:
            rec = lenb - lenc
            vb  = vb ^ (vc << rec)
            vq |= (1 << rec)
            lenb = vb.bit_length()

        result.append(self.n2s(vq))
        result.append(self.n2s(vb))
        return result 
    
    def gcd(self,a,b):
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        x1,y1 =1,0
        x2,y2 =0,1
        while n_b:
            q,r = self.div(n_a,n_b)
            n_a,n_b = n_b,self.s2n(r)
            x1,x2 = x2,x1 ^ self.s2n(self.modmult(q,self.n2s(x2),self.para.p))
            y1,y2 = y2,y1 ^ self.s2n(self.modmult(q,self.n2s(y2),self.para.p))
            
        return self.n2s(n_a)
    
    def modinv(self,a,m): 
        s_m = m
        x1,x2 = 1,0
        while self.s2n(m):
            q,r = self.div(a,m)
            a,m = m,r
            x1,x2 = x2,x1 ^ self.s2n(self.modmult(q,self.n2s(x2),s_m))
        return self.n2s(x1)
    
    def add(self,a,b):
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        n_a = n_a ^ n_b
        return self.n2s(n_a)
    '''
    仿射
    y^2 + xy = x^3 + ax^2 + b
    '''
    
    '''
    仿射坐标点加运算
    nmd = (y1+y2)/(x1+x2)
    x3 = nmd^2 + nmd + x1 + x2 + a
    y3 = (x3 + x1) * nmd + x3 + y1
    '''
    def affine_point_add(self,pa,pb,para):
        p = para.p
        inv=self.modinv(self.add(pa.x,pb.x),p)
        nmd=self.modmult(self.add(pa.y,pb.y), inv,p)
        nmd2=self.modmult(nmd, nmd,p)
        x3=self.add(nmd2,nmd)
        x3=self.add(x3,pa.x)
        x3=self.add(x3,pb.x)
        x3=self.add(x3,para.a)
        y3=self.add(pa.x,x3)
        y3=self.modmult(y3,nmd,p)
        y3=self.add(y3,x3)
        y3=self.add(y3,pa.y)
        
        r_point=point()
        r_point.x = x3
        r_point.y = y3
        return r_point
    
    '''
    
    仿射坐标倍点运算
    nmd = x1 + y1/x1
    x2 = nmd^2 + nmd + a
    y2 = x1^2 + (nmd+1)*x2
    '''
    def affine_point_dbl(self,pa,para):
        p=para.p
        inv=self.modinv(pa.x,p)
        nmd=self.add(pa.x,self.modmult(pa.y, inv,p))
        nmd2=self.modmult(nmd,nmd,p)
        x2=self.add(nmd2,nmd)
        x2=self.add(x2,para.a)
        t=self.add(nmd,"1")
        t=self.modmult(t, x2,p)
        y2=self.modmult(pa.x,pa.x,p)
        y2=self.add(y2,t)
        r_point=point()
        r_point.x = x2
        r_point.y = y2
        return r_point
    
    '''
    射影坐标
    y^2z + xyz = x^3 + ax^2 + bz^3  b!=0
    
    当z!=0 
    X = x/z
    Y = y/z 可转换到仿射坐标系
    '''
    
    '''
    标准射影坐标倍点运算
    '''
    def sprojective_point_dbl(self,pa,z,para):
        x1=pa.x
        y1=pa.y
        z1=z
        p=para.p
        a=para.a
        
        # t1 = x1 * z1
        t1 = self.modmult(x1,z1,p)
        
        # t2 = x1 *x1
        t2 = self.modmult(x1,x1,p)
        
        # t3 = t2 + y1*z1
        t3 = self.modmult(y1,z1,p)
        t3 = self.add(t3,t2)
        
        # t4 = t1 ^2
        t4 = self.modmult(t1,t1,p)
        
        # t5 = t3 * (t1 + t3) + a * t4
        t5 = self.add(t1,t3)
        t5 = self.modmult(t5,t3,p)
        tmp = self.modmult(a,t4,p)
        t5 = self.add(t5,tmp)  
        
        # x3 = t1 * t5
        x3 = self.modmult(t1,t5,p)
        
        # y3 = t2^2 * t1 + t3*t5 + x3
        y3 = self.modmult(t2,t2,p)
        y3 = self.modmult(y3,t1,p)
        tmp = self.modmult(t3,t5,p)
        y3 = self.add(y3,tmp)
        y3 = self.add(y3,x3)
        
        # z3 = t1 *t4
        z3 = self.modmult(t1,t4,p)
        
       
        # 射影坐标系转化成仿射坐标系
        return self.sprojective_to_affine(x3,y3,z3,para)
        
    '''
    标准射影坐标点加运算
    '''
    def sprojective_point_add(self,pa,za,pb,zb,para):
        x1=pa.x
        y1=pa.y
        z1=za
        x2=pb.x
        y2=pb.y
        z2=zb
        p=para.p
        a=para.a
        
        if x1 == "0" and y1 == "1" and z1 == "0":
            r_point = pb
            r_point.z = "1"
            return r_point
        elif x2 == "0" and y2 == "1" and z2 =="0":
            r_point = pa
            r_point.z = "1"
            return r_point
        
        # t1 = x1*z2
        t1 = self.modmult(x1,z2,p)
        
        # t2 = x2*z1
        t2 = self.modmult(x2,z1,p)
        
        # t3 = t1 + t2
        t3 = self.add(t1,t2)
        
        # t4 = y1*z2
        t4 = self.modmult(y1,z2,p)
        
        # t5 = y2*z1
        t5 = self.modmult(y2,z1,p)
        
        # t6 = t4 + t5
        t6 = self.add(t4,t5)
        
        # t7 = z1*z2
        t7 = self.modmult(z1,z2,p)
        
        # t8 = t3^2
        t8 = self.modmult(t3,t3,p)
        
        # t9 = t8 * t7
        t9 = self.modmult(t8,t7,p)
        
        # t10 = t3 * t8
        t10 = self.modmult(t3,t8,p)
        
        # t11 = t6 * t7 * (t6 + t3) + t10 + a * t9
        t11 = self.modmult(t6,t7,p)
        tmp = self.add(t6,t3)
        t11 = self.modmult(t11,tmp,p)
        t11 = self.add(t11,t10)
        tmp = self.modmult(a,t9,p)
        t11 = self.add(t11,tmp)
        
        # x3 = t3 * t11
        x3 = self.modmult(t3,t11,p)
        
        # y3 = t6 *(t1*t8+t11) + x3 + t10 * t4
        y3 = self.modmult(t1,t8,p)
        y3 = self.add(y3,t11)
        y3 = self.modmult(t6,y3,p)
        y3 = self.add(y3,x3)
        tmp =self.modmult(t10,t4,p)
        y3 = self.add(y3,tmp)
        
        # z3 = t3 * t9
        z3 = self.modmult(t3,t9,p)
        
        # 射影坐标系转化成仿射坐标系
        return self.sprojective_to_affine(x3,y3,z3,para)
    
    def sprojective_to_affine(self,x,y,z,para):  
        p = para.p
        #(z^-1)
        zinv = self.modinv(z,p)
        
        #x3=x*(z^-1)        
        x3 = self.modmult(x,zinv,p)
        
        #y3=y*(z^-1)        
        y3 = self.modmult(y,zinv,p)
        
        r_point = point()
        r_point.x = x3
        r_point.y = y3
        return r_point  
    
    '''
    jacobian加重射影坐标
    y^2 + xyz = x^3 + ax^2z^2 + bz^6  b!=0
    
    当z!=0 
    X = x/z^2
    Y = y/z^3 可转换到仿射坐标系
    '''
    def jacobian_to_affine(self,x,y,z,para):
        p = para.p
        #(z^-3)
        t4 = self.modmult(z,z,p)
        t4 = self.modmult(t4,z,p)
        t4 = self.modinv(t4,p)
        
        #y=Y/(z^3)        
        t2 = self.modmult(y,t4,p)
        
        #x=X/(z^2)=X*(z^-3)(z)
        t4 = self.modmult(t4,z,p)
        t1 = self.modmult(x,t4,p)
        
        r_point = point()
        r_point.x = t1
        r_point.y = t2
        return r_point
    
    def jacobian_point_dbl(self,pa,z,para):
        x1 = pa.x
        y1 = pa.y
        z1 = z
        p = para.p
        a = para.a
        b = para.b
        
        # z3=x1*z1^2
        z3 = self.modmult(z1,z1,p)
        z3 = self.modmult(z3,x1,p)
        
        # x3 = x1^4 + bz1^8
        x3 = self.modmult(x1,x1,p)
        x3 = self.modmult(x3,x3,p)
        tmp= self.modmult(z1,z1,p)
        tmp = self.modmult(tmp,tmp,p)
        tmp = self.modmult(tmp,tmp,p)
        tmp = self.modmult(tmp,b,p)
        x3 = self.add(x3,tmp)
        
        # t1 = z3 + x1^2 + y1*z1
        t1 = self.modmult(x1,x1,p)
        t1 = self.add(t1,z3)
        tmp=self.modmult(y1,z1,p)
        t1 = self.add(t1,tmp)

        # y3= x1^4 * z3 + t1 * x3
        y3 = self.modmult(x1,x1,p)
        y3 = self.modmult(y3,y3,p)
        y3 = self.modmult(y3,z3,p)
        tmp = self.modmult(t1,x3,p)
        y3 = self.add(y3,tmp)
        
        return self.jacobian_to_affine(x3,y3,z3,para)
    
    def jacobian_point_add(self,pa,za,pb,zb,para):
        r_point = point()
        p = para.p
        x1 = pa.x
        y1 = pa.y
        z1 = za
        x2 = pb.x
        y2 = pb.y
        z2 = zb
        a = para.a
        b = para.b
        
        if x1 == "1" and y1 == "1" and z1 == "0":
            r_point = pb
            r_point.z = "1"
            return r_point
        elif x2 == "1" and y2 == "1" and z2 =="0":
            r_point = pa
            r_point.z = "1"
            return r_point
        
        # t1 = x1 * z2^2
        t1 = self.modmult(x1,z2,p)
        t1 = self.modmult(t1,z2,p)
        
        # t2 = x2 * z1^2
        t2 = self.modmult(x2,z1,p)
        t2 = self.modmult(t2,z1,p)
        
        # t3 = t1 + t2
        t3 = self.add(t1,t2)
        
        # t4 = y1 * z2^3
        t4 = self.modmult(y1,z2,p)
        t4 = self.modmult(t4,z2,p)
        t4 = self.modmult(t4,z2,p)
        
        #t5 = y2 * z1^3
        t5 = self.modmult(y2,z1,p)
        t5 = self.modmult(t5,z1,p)
        t5 = self.modmult(t5,z1,p)
        
        # t6 = t4 + t5
        t6 = self.add(t4,t5)
        
        # t7 = z1*t3
        t7 = self.modmult(z1,t3,p)
        
        # t8 = t6*x2 + t7 * y2
        t8 = self.modmult(t6,x2,p)
        t8 = self.add(t8,self.modmult(t7,y2,p))
        
        # z3 = t7 * z2
        z3 = self.modmult(t7,z2,p)
        
        # t9 = t6 + z3
        t9 = self.add(t6,z3)
        
        # x3 = a*z3^2 + t9*t6 + t3^3
        x3 = self.modmult(z3,z3,p)
        x3 = self.modmult(x3,a,p)
        x3 = self.add(x3,self.modmult(t9,t6,p))
        tmp = self.modmult(t3,t3,p)
        tmp = self.modmult(tmp,t3,p)
        x3 = self.add(x3,tmp)
        
        # y3 = t9*x3+t8*t7^2
        y3 = self.modmult(t9,x3,p)
        tmp = self.modmult(t7,t7,p)
        tmp = self.modmult(tmp,t8,p)
        y3 = self.add(y3,tmp)
        
        return self.jacobian_to_affine(x3,y3,z3,para)
        

    '''仿射坐标下二进制展开法多倍点运算'''
    def point_mult(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        p = pa
        for i in bin_k[3:]:
            p = self.affine_point_dbl(p,para)
            if i == "1":    
                p = self.affine_point_add(p,pa,para)
        return p

    def point_mult2(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        r_bin_k =[]
        for i in range(len(bin_k[3:])):
            r_bin_k.append(bin_k[len(bin_k)-2-i])

        if bin_k[len(bin_k)-1] == "1":    
            p = pa
            p.z = "1"
        else:
            p = point()
            p.x = "0"
            p.y = "1"
            p.z = "0"
        q = pa
        for i in r_bin_k:
            q = self.sprojective_point_dbl(q,"1",para)
            if i == "1":     
                p = self.sprojective_point_add(p,p.z,q,"1",para)
                p.z = "1"
        return p

    def point_mult3(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        p = pa
        for i in bin_k[3:]:
            p = self.sprojective_point_dbl(p,"1",para)
            if i == "1":    
                p = self.sprojective_point_add(p,"1",pa,"1",para)
        return p
    
    def point_mult4(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        p = pa
        for i in bin_k[3:]:
            p = self.jacobian_point_dbl(p,"1",para)
            if i == "1":    
                p = self.jacobian_point_add(p,"1",pa,"1",para)
        return p
    
    def point_mult5(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        r_bin_k =[]
        for i in range(len(bin_k[3:])):
            r_bin_k.append(bin_k[len(bin_k)-2-i])
        
        if bin_k[len(bin_k)-1] == "1":    
            p = pa
            p.z = "1"
        else:
            p = point()
            p.x = "1"
            p.y = "1"
            p.z = "0"
        q = pa
        for i in r_bin_k:
            q = self.jacobian_point_dbl(q,"1",para)
            if i == "1":     
                p = self.jacobian_point_add(p,p.z,q,"1",para)
                p.z = "1"
        return p
    

class NN:
    def __init__(self):
        self.para = ecc_para()
    
    def s2n(self,v):
        return int(v,16) 
        
    def n2s(self,n):
        return hex(n).replace("0x","")
    
    '''
    mult a = b * c
    c = k0*2^0 + k1*2^1 + ... + kn-1 * 2^(n-1)
    a = b * c 
      = b * (k0*2^0 + k1*2^1 + ... + kn-1 * 2^(n-1))
    '''
    def mult(self,b,c):
        n_a = self.s2n(b) * self.s2n(c) 
        return self.n2s(n_a)
    
    '''
    商和余数
    '''
    def div(self,b,c):
        result=[]
        n_p = self.s2n(b) // self.s2n(c)
        n_q = self.s2n(b) %  self.s2n(c)
        result.append(self.n2s(n_p))
        result.append(self.n2s(n_q))
        return result 
    
    def add(self,a,b):
        return self.n2s(self.s2n(a) + self.s2n(b))
    
    def sub(self,a,b):
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        if n_a > n_b:
            return self.n2s(self.s2n(a) - self.s2n(b))
        else:
            n_c = n_b - n_a
            n_c_inv = ~n_c + 1
            return self.n2s(n_c_inv)
    
    def gcd(self,a,b):
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        while n_a != 0:
            n_a,n_b = n_b%n_a,n_a
        return self.n2s(n_b)
    
    def modsub(self,a,b,p):
        #a<b, (a-b)mod p = (p-(b-a) mod p)
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        if n_a >= n_b:
           c = self.sub(a,b)
           return self.div(c,p)[1]
        else:
           c =  self.sub(b,a)
           c = self.div(c,p)[1]
           return self.sub(p,c)
         
        
    def modadd(self,a,b,p):
        c = self.add(a,b)
        return self.div(c,p)[1]
    
    def modinv(self,a,m): 
        n_a = self.s2n(a)
        n_m = self.s2n(m)
           
        if self.gcd(a,m) != "1":
            return None
        u1,u2,u3 = 1,0,n_a
        v1,v2,v3 = 0,1,n_m
        while v3 != 0:
            q = u3//v3
            v1,v2,v3,u1,u2,u3 =(u1-q*v1),(u2-q*v2),(u3-q*v3),v1,v2,v3
        return self.n2s(u1%n_m)
    
    def modmult(self,a,b,p):       
        c = self.mult(a,b)        
        ret = self.div(c,p)
        return ret[1]
    
    #b^exp mod(p) 
    def modexp(self,b, exp, p):
        result = "1"
        e = self.s2n(exp)
        b1 = b
        while e != 0:
            if (e&1) == 1:
                # ei = 1, then mul
                result = self.modmult(result,b1,p)
            e >>= 1
            # b, b^2, b^4, b^8, ... , b^(2^n)
            b1 = self.modmult(b1,b1,p)
        return result
    
    '''
    x/r (mod n)
    '''
    def mon_reduction(self,x,r,n):
        n_r = self.s2n(r)
        n_n = self.s2n(n)
        m = self.modinv(n,r)
        m = self.modmult(x,m,r)
        t = self.mult(m,n)
        y = self.sub(x,t)
        n_y = self.s2n(y)
        n_y = n_y >> (len(bin(n_r)) - 2 - 1)
        if n_y > n_n:
            n_y = n_y - n_n
        return self.n2s(n_y)
    
    

    def mon_modmult(self,a,b,p):
        n_a = self.s2n(a)
        n_b = self.s2n(b)
        n_p = self.s2n(p)
        pass
    
    def affine_point_dbl(self,pa,para):
        a = para.a
        x = pa.x
        y = pa.y
        p = para.p
        #m=3x^2+a / 2y
        t1 = self.modmult(y,"2",p)
        t1 = self.modinv(t1,p)
        m = self.modmult(x,x,p)
        m = self.modmult(m,"3",p)
        m = self.modadd(m,a,p)
        m = self.modmult(m,t1,p)
        
        x2 = self.modmult(m,m,p)
        x2 = self.modsub(x2,x,p)
        x2 = self.modsub(x2,x,p)
        
        y2 = self.modsub(x,x2,p)
        y2 = self.modmult(y2,m,p)
        y2 = self.modsub(y2,y,p)
        
        r_point=point()
        r_point.x = x2
        r_point.y = y2
        return r_point
    
    def affine_point_add(self,pa,pb,para):
        a = para.a
        x = pa.x
        y = pa.y
        xb = pb.x
        yb = pb.y
        p = para.p
        
        #m=(yp-yq) / (xp-xq)
        t1 = self.modsub(x,xb,p)
        t1 = self.modinv(t1,p)
        
        m = self.modsub(y,yb,p)
        m = self.modmult(m,t1,p)
        
        x2 = self.modmult(m,m,p)
        x2 = self.modsub(x2,x,p)
        x2 = self.modsub(x2,xb,p)
        
        y2 = self.modsub(x,x2,p)
        y2 = self.modmult(y2,m,p)
        y2 = self.modsub(y2,y,p)
        
        r_point=point()
        r_point.x = x2
        r_point.y = y2
        return r_point
    
    def jacobian_to_affine(self,x,y,z,para):
        p = para.p
        #(z^-3)
        t4 = self.modmult(z,z,p)
        t4 = self.modmult(t4,z,p)
        t4 = self.modinv(t4,p)
        
        #y=Y/(z^3)        
        t2 = self.modmult(y,t4,p)
        
        #x=X/(z^2)=X*(z^-3)(z)
        t4 = self.modmult(t4,z,p)
        t1 = self.modmult(x,t4,p)
        
        r_point = point()
        r_point.x = t1
        r_point.y = t2
        return r_point
    
    '''
    曲线参数：雅可比坐标系
        曲线: y^2 = x^3 + ax + b
    '''
    def jacobian_point_dbl(self,pa,z,para):
        # m = 3 * x^2 + a *z^4
        p = para.p
        t1 = pa.x
        t2 = pa.y
        t3 = z
        t4 = para.a
        t5 = self.modmult(t3,t3,p)
        t5 = self.modmult(t5,t5,p)
        t5 = self.modmult(t4,t5,p)
        t4 = self.modmult(t1,t1,p)
        t4 = self.modmult(t4,"3",p)
        t4 = self.modadd(t4,t5,p)
        
        #Z2 = 2*Y*Z
        t3 = self.modmult(t2,t3,p)
        t3 = self.modmult(t2,"2",p)
        
        #S = 4*x*Y^2
        t2 = self.modmult(t2,t2,p)
        t5 = self.modmult(t1,t2,p)
        t5 = self.modmult(t5,"4",p)
        
        #X2 = M^2-2S
        t1 = self.modmult(t4,t4,p)
        t6 = self.modmult(t5,"2",p)
        t1 = self.modsub(t1,t6,p)
        
        #T=8Y^4
        t2 = self.modmult(t2,t2,p)
        t2 = self.modmult(t2,"8",p)
        
        #Y2=M*(S-X2)-T
        t5 = self.modsub(t5,t1,p)
        t5 = self.modmult(t5,t4,p)
        t2 = self.modsub(t5,t2,p)
        
        # 射影坐标系转化成仿射坐标系
        return self.jacobian_to_affine(t1,t2,t3,para)
        
    def jacobian_point_add(self,pa,za,pb,zb,para):
        r_point = point()
        p = para.p
        t1 = pa.x
        t2 = pa.y
        t3 = za
        t4 = pb.x
        t5 = pb.y
        
        t6 = zb
        
        if t1 == "1" and t2 == "1" and t3 == "0":
            r_point = pb
            r_point.z = "1"
            return r_point
        elif t4 == "1" and t5 == "1" and t6 =="0":
            r_point = pa
            r_point.z = "1"
            return r_point
        
        #U0 = x0*z1^2
        t7 = self.modmult(t6,t6,p)
        t1 = self.modmult(t1,t7,p)
        
        #S0 = y0*z1^3
        t7 = self.modmult(t6,t6,p)
        t2 = self.modmult(t2,t7,p)
        
        #U1 = x1*z0^2
        t7 = self.modmult(t3,t3,p)
        t4 = self.modmult(t4,t7,p)
        
        #S1 = y1*z0^3
        t7 = self.modmult(t3,t7,p)
        t5 = self.modmult(t5,t7,p)
        
        #W= U0-U1
        t4 = self.modsub(t1,t4,p)
        
        #R=S0-S1
        t5 = self.modsub(t2,t5,p)
        
        #T=U0+U1
        if self.s2n(t4)== 0:
            if self.s2n(t5) == 0:
                r_point.x = 0
                r_point.y = 0
            else:
                r_point.x = 1
                r_point.y = 1
            return r_point
        t7 = self.modmult(t1,"2",p)
        t1 = self.modsub(t7,t4,p)
          
        #M=S0+S1
        t7 = self.modmult(t2,"2",p)
        t2 = self.modsub(t7,t5,p)
        
        #Z2 = Z0*Z1*W
        t3 = self.modmult(t3,t6,p)
        t3 = self.modmult(t3,t4,p)
        
        #X2 = R^2-T*W^2
        t7 = self.modmult(t4,t4,p) # W^2
        t4 = self.modmult(t4,t7,p) # W^3
        t7 = self.modmult(t1,t7,p) # T*W^2
        t1 = self.modmult(t5,t5,p) # R^2
        t1 = self.modsub(t1,t7,p)  # R2 - T*W^2
        
        #V = T*W^2-2*X2
        t8 = self.modmult(t1,"2",p)# 2*X2
        t7 = self.modsub(t7,t8,p)  # T*W^2 - 2*X2
        
        #2*Y2=V*R-M*W^3
        t5 = self.modmult(t5,t7,p) # V*R
        t4 = self.modmult(t2,t4,p) # M*W^3
        t2 = self.modsub(t5,t4,p)  # V*R - M*W^3
        
        t4 = self.modinv("2",p)
        t2 = self.modmult(t4,t2,p)
        
        # 射影坐标系转化成仿射坐标系
        return self.jacobian_to_affine(t1,t2,t3,para)
    
    def point_mult(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        p = pa
        for i in bin_k[3:]:
            p = self.affine_point_dbl(p,para)
            if i == "1":    
                p = self.affine_point_add(p,pa,para)
        return p
    
    def point_mult1(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        r_bin_k =[]
        for i in range(len(bin_k[3:])):
            r_bin_k.append(bin_k[len(bin_k)-2-i])
        
        if bin_k[len(bin_k)-1] == "1":    
            p = pa
            flag = 1
        else:
            flag = 0
        q = pa
        for i in r_bin_k:
            q = self.affine_point_dbl(q,para)
            if i == "1":  
                if flag == 0:
                   flag = 1
                   p = q
                   continue   
                p = self.affine_point_add(p,q,para)
        return p
    
    def point_mult2(self,pa,k,para):
        n_k = self.s2n(k)
        bin_k = bin(n_k)
        r_bin_k =[]
        for i in range(len(bin_k[3:])):
            r_bin_k.append(bin_k[len(bin_k)-2-i])
        
        if bin_k[len(bin_k)-1] == "1":    
            p = pa
            p.z = "1"
        else:
            p = point()
            p.x = "1"
            p.y = "1"
            p.z = "0"
        q = pa
        for i in r_bin_k:
            q = self.jacobian_point_dbl(q,"1",para)
            if i == "1":     
                p = self.jacobian_point_add(p,p.z,q,"1",para)
                p.z = "1"
        return p
    '''
    判断 点是否在曲线上
        y^2 = x^3 + ax +b
    '''
    def verifypoint(self,pa,para):
        p = para.p
        x = pa.x
        y = pa.y
        a = para.a
        b = para.b
        
        # t1 = y^2
        t1 = self.modmult(y,y,p)
        
        # t2 = x^3 
        t2 = self.modmult(x,x,p)
        t2 = self.modmult(t2,x,p)
        
        # t3 = ax
        t3 = self.modmult(a,x,p)
        
        # t2 = x^3 + ax
        t2 = self.modadd(t2,t3,p)
        
        # t2 = x^3 + ax + b
        t2 = self.modadd(t2,b,p)
        
        if t1 == t2:
            return True
        else:
            return False
ecc = NN_2m()
ecc.para.p ="20000000000000000000000000000000000000000000000000000000000001001"         
ecc.para.a ="0"
ecc.para.b ="00E78BCD09746C202378A7E72B12BCE00266B9627ECB0B5A25367AD1AD4CC6242B"
ecc.para.g.x = "00CDB9CA7F1E6B0441F658343F4B10297C0EF9B6491082400A62E7A7485735FADD"
ecc.para.g.y = "013DE74DA65951C4D76DC89220D5F7777A611B1C38BAE260B175951DC8060C2B3E"

ecc.para.prikey = "00771ef3dbff5f1cdc32b9c572930476191998b2bf7cb981d7f5b39202645f0931"
ecc.para.pubkey.x="165961645281a8626607b917f657d7e9382f1ea5cd931f40f6627f357542653b2"
ecc.para.pubkey.y="1686522130d590fb8de635d8fca715cc6bf3d05bef3f75da5d543454448166612"

ecc.para.prikey = "00771ef3dbff5f1cdc32b9c572930476191998b2bf7cb981d7f5b39202645f0930"
p = ecc.point_mult(ecc.para.g,ecc.para.prikey,ecc.para)
print("p.x:",p.x)
print("p.y:",p.y)

p = ecc.point_mult2(ecc.para.g,ecc.para.prikey,ecc.para)
print("p.x:",p.x)
print("p.y:",p.y)