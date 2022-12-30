	.file	"debug_functions.c"
	.intel_syntax noprefix
	.text
	.globl	__PRINTU__
	.type	__PRINTU__, @function
__PRINTU__:
	sub	rsp, 40
	mov	ecx, 1
	mov	r9d, 31
	mov	r8d, 10
	mov	BYTE PTR 31[rsp], 10
.L2:
	movzx	eax, cx
	mov	esi, r9d
	xor	edx, edx
	inc	ecx
	sub	esi, eax
	mov	rax, rdi
	div	r8
	movsx	rsi, esi
	add	edx, 48
	mov	BYTE PTR [rsp+rsi], dl
	mov	rdx, rdi
	mov	rdi, rax
	cmp	rdx, 9
	ja	.L2
	movzx	edx, cx
	mov	eax, 32
	movzx	ecx, cx
	mov	edi, 1
	sub	eax, ecx
	cdqe
	lea	rsi, [rsp+rax]
	call	write@PLT
	add	rsp, 40
	ret
	.size	__PRINTU__, .-__PRINTU__
	.section	.text.startup,"ax",@progbits
	.globl	main
	.type	main, @function
main:
	push	rax
	mov	edi, 10974123
	call	__PRINTU__
	mov	edi, 1937
	call	__PRINTU__
	mov	edi, 420
	call	__PRINTU__
	mov	edi, 69
	call	__PRINTU__
	xor	edi, edi
	call	__PRINTU__
	xor	eax, eax
	pop	rdx
	ret
	.size	main, .-main
	.ident	"GCC: (GNU) 12.2.0"
	.section	.note.GNU-stack,"",@progbits
