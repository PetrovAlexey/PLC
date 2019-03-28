fbeg fibbonachi
mov *ex **sp
pop
mov *ax **sp
pop
mov *bx **sp
pop
mov *fx **sp
pop
goto *fx 4
push *bx
push *ax
mov *ip *ex
sub *fx 1
push *ex
push *fx
push *bx
push *ax
call fibbonachi
mov *ax **sp
pop
mov *bx **sp
pop
mov *cx *bx
add *bx *ax
mov *ax *cx
mov *ex **sp
pop
push *bx
push *ax
mov *ip *ex
fend
putstr Programm counting n's number of Fibonachi
putstr print n:
read *ax
push *ax
push 1
push 0
call fibbonachi
mov *ax **sp
pop
mov *bx **sp
pop
putstr Number equals:
print *bx
stop
