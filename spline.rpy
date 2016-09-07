#スプライン補間用の関数を追加します。
# Add the function for spline interpolation.
# _spline(sp, x)
#  タプル(x, y)のリストからスプライン補間を用いてxに対応する値を返します。
# sp: タプル(x, y)のリスト
#  x: 求めるxの値




# init -1 python:
#     class _Spline():
#         def __init__(self, sp):
#             self.sp = sp
#             self.num = len(sp)-1
#             MaxSplineSize = self.num + 1
#             self.a = [0]*MaxSplineSize
#             self.b = [0]*MaxSplineSize
#             self.c = [0]*MaxSplineSize
#             self.d = [0]*MaxSplineSize
#
#             w = [0]*MaxSplineSize
#             for i in range(0, self.num+1):
#                 self.a[i] = sp[i][0]
#
#             self.c[0] = self.c[self.num] = 0.0
#             for i in range(1, self.num):
#                 self.c[i] = 3.0 * (self.a[i+1] - self.a[i])/float(sp[i+1][1]-sp[i][1]) - 3.0 * (self.a[i]-self.a[i-1])/float(sp[i][1]-sp[i-1][1])
#             w[0]=0.0
#             for i in range(1, self.num):
#                 tmp = 2*(sp[i+1][1]-sp[i-1][1]) - w[i-1]
#                 self.c[i] = (self.c[i] - (sp[i][1]-sp[i-1][1])*self.c[i-1])/float(tmp)
#                 w[i] = (sp[i+1][1]-sp[i][1]) / float(tmp)
#             for i in range(self.num-1, 0, -1):
#                 self.c[i] = self.c[i] - self.c[i+1] * w[i]
#
#             self.b[self.num] = self.d[self.num] =0.0
#             for i in range(0, self.num):
#                 self.d[i] = ( self.c[i+1] - self.c[i]) / (3.0*(sp[i+1][1]-sp[i][1]))
#                 self.b[i] = (self.a[i+1] - self.a[i])/float(sp[i+1][1]-sp[i][1]) - (sp[i+1][1]-sp[i][1])*(self.c[i+1]+2.0*self.c[i])/3.0
#
#         def culc(self, t):
#             for i in range(0, len(self.sp)):
#                 if t < self.sp[i][1]:
#                     j = i - 1
#                     break
#             else:
#                 j = len(self.sp) - 2
#
#             dt = float(t) - float(j);
#             return self.a[j] + ( self.b[j] + (self.c[j] + self.d[j] * dt) * dt ) * dt
init python:
    def _spline(sp, x):
    
    # スプライン補間関数
    # sp    : [(x, y)]既知の点群
    # x      : xの値
    # 戻り値 : xに対応する関数の値
        N = len(sp)
        idx = -1
        h = [0]*(N-1)
        b = [0]*(N-1)
        d = [0]*(N-1)
        g = [0]*(N-1)
        u = [0]*(N-1)
        r = [0]*(N)

        i = 1
        while(i<N-1 and idx<0):
            if x < sp[i][0]:
                idx = i - 1
            i += 1
        
        if idx < 0:
            idx = N-2
        
        for i in range(0, N-1):
            h[i] = sp[i+1][0] - sp[i][0];

        for i in range(1, N-1):
            b[i] = 2.0 * (h[i] + h[i-1])
            d[i] = 3.0 * ((sp[i+1][1] - sp[i][1]) / h[i] - (sp[i][1] - sp[i-1][1]) / h[i-1])

        g[1] = h[1] / b[1]

        for i in range(2, N-2):
            g[i] = h[i] / (b[i] - h[i-1] * g[i-1])

        u[1] = d[1] / b[1]

        for i in range(2, N-1):
            u[i] = (d[i]-h[i-1] * u[i-1]) / (b[i] - h[i-1] * g[i-1])
        
        if idx > 1:
            k = idx
        else:
            k = 1

        r[0]   = 0.0
        r[N-1] = 0.0
        r[N-2] = u[N-2]
        
        for i in range(N-3, k, -1):
            r[i] = u[i] - g[i] * r[i+1]

        dx = x - sp[idx][0];
        q = (sp[idx+1][1] - sp[idx][1]) / h[idx] - h[idx] * (r[idx+1] + 2.0 * r[idx]) / 3.0
        s = (r[idx+1] - r[idx]) / (3.0 * h[idx])
        
        return sp[idx][1] + dx * (q + dx * (r[idx]  + s * dx))
