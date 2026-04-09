# DocVault — FAQ / الأسئلة الشائعة

## General / عام

**Q: What file types does DocVault support?**
A: DocVault manages any file type that Frappe supports (PDF, DOCX, XLSX, images, etc.). It stores metadata in DV Document while the actual file is managed by Frappe's File system.

**س: ما أنواع الملفات التي يدعمها DocVault؟**
ج: يدير DocVault أي نوع ملف يدعمه Frappe (PDF، DOCX، XLSX، صور، إلخ). يخزن البيانات الوصفية في DV Document بينما يدير نظام ملفات Frappe الملف الفعلي.

---

**Q: How does document versioning work?**
A: Each time a new file is uploaded for an existing document, a DV Version record is created with the version number, file URL, and change notes. The document's version_number field is automatically incremented.

**س: كيف يعمل إصدار المستندات؟**
ج: في كل مرة يتم فيها رفع ملف جديد لمستند موجود، يتم إنشاء سجل DV Version برقم الإصدار ورابط الملف وملاحظات التغيير. يتم زيادة حقل version_number تلقائياً.

---

**Q: What is check-in/check-out?**
A: Check-out locks a document so only one person can edit it at a time. Once their changes are uploaded, they check the document back in, releasing the lock.

---

**Q: How do retention policies work?**
A: Define retention policies per category with retention days. The RetentionService runs daily to flag documents past their retention date for review or automatic archival.

---

**Q: Can external users access documents?**
A: Yes. The DV Portal module provides controlled access for external users. Administrators define which documents are portal-accessible and track downloads via DV Download Log.
