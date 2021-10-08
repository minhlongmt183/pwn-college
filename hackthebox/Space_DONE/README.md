# Space
---

```c
int main(void)

{
  undefined local_2f [31];
  undefined *local_10;
  
  local_10 = &stack0x00000004;
  printf("> ");
  fflush(stdout);
  read(0,local_2f,0x1f);
  vuln(local_2f);
  return 0;
}
```
- đọc 31 byte
- hàm vuln
```cpp
void vuln(char *param_1)

{
  char local_12 [10];
  
  __x86.get_pc_thunk.ax();
  strcpy(local_12,param_1);
  return;
}
```


 EAX  0xffffd46a ◂— 'AAAAAAAAa\n'
 EBX  0x804b200 (_DYNAMIC+44) —▸ 0x804b1d0 (__do_global_dtors_aux_fini_array_entry) —▸ 0x8049160 (__do_global_dtors_aux) ◂— cmp    byte ptr [0x804b2ec], 0
 ECX  0xffffd491 ◂— 'AAAAAAAAa\n'
 EDX  0xffffd46a ◂— 'AAAAAAAAa\n'
 EDI  0xf7fab000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1ead6c
 ESI  0xf7fab000 (_GLOBAL_OFFSET_TABLE_) ◂— 0x1ead6c
*EBP  0xffffd4b8 ◂— 0x0
*ESP  0xffffd47c —▸ 0x8049231 (main+98) ◂— add    esp, 0x10
*EIP  0x80491ce (vuln+42) ◂— ret    

- Với read, khi nhập hơn 32 kí tự, nó sẽ còn nằm trên stdin, nếu gọi read 1 lần nữa, nó sẽ ghi hét phần còn lại vào 
- Ta chia payload thành 2 phần, phần 1 chạy và nhảy tới lệnh read 1 lần nữa để đọc dữ 1 lần nữa và payload2 lưu mã khai thác

- flag: HTB{sh3llc0de_1n_7h3_5p4c3}