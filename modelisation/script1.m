%%%%%%%%%%%%%%%%%%%%TD1
%%%%%%%%%%%%%%%%%%%%1)

Fs.num=[5];
Fs.den=[3, 1];

Te=3/5; %période d'échantillonage

F4=tf(Fs.num, Fs.den);

%%%%%%%%%%%%%%%%%%%%2)
%taille des matrices
Fs.numLenght=size(Fs.num);
Fs.denLenght=size(Fs.den);

DenDegres=Fs.denLenght(1,2)-1;
NumDegres=Fs.numLenght(1,2)-1;

%matrice B
B=zeros(DenDegres,1);
B(DenDegres, 1)=1/Fs.den(1,1);

%matrice C
C=zeros(1,DenDegres);
for i=1:(NumDegres+1)
    C(1,i)=Fs.num(1,NumDegres-i+2);
end
%flip([1,2,3,4])=[4,3,2,1]

%matrice A
c=2;
A=zeros(DenDegres,DenDegres);
for i=1:DenDegres-1
    A(i,c)=1;
    c=c+1;
end
an=Fs.den(Fs.denLenght(1,1));
for i=1:DenDegres
   A(DenDegres,i)=-Fs.den(1,DenDegres-i+2)/an;
end

%%%%%%%%%%%%%%%%%%%%TD2

%matrice M

M=zeros(DenDegres+1,DenDegres+1);
M(1:DenDegres,1:DenDegres+1)= [A,B];


%exponentielle



E = expm(M*Te);

Ad=E(1:DenDegres, 1:DenDegres);

Bd=E(1:DenDegres, DenDegres+1);

[Nz,Dz]=extractFdt(Ad,Bd,C);

% this script accepts as inputs the matrix Ad and the vectors Bd and C,
% where EXP([A,B;0,0]*t)=[Ad,Bd;0,1], and gives as output two vectors
% [out1,out2], out1 being the numerator of the transfer function of the
% sampled system, out2 being its denominator. They can be directly read by
% Simulink
function [out1,out2]=extractFdt(Ad,Bd,C)
syms z;
n=size(Ad)*[1;0];
Fz = C*(eye(n)*z-Ad)^(-1)*Bd;

[N,D]=numden(Fz);

Dpz=coeffs(D);
out1 = double(coeffs(N)/Dpz(n+1));
out2 = double(Dpz/Dpz(n+1));


out2=flip(out2);

out1=flip(out1);

end
