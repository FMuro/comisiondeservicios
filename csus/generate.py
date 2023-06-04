from docxtpl import DocxTemplate

doc = DocxTemplate("cservicio.docx")
context = {'solicitante': "Fernando Muro Jiménez"}
doc.render(context)
doc.save("generated_doc.docx")
