from pathlib import Path
from zipfile import ZipFile,ZIP_DEFLATED
root=Path(__file__).resolve().parents[2]
out=root/'downloads/chemistry-co2-panorama-v2.zip'
with ZipFile(out,'w',ZIP_DEFLATED,compresslevel=9) as z:
    z.write(root/'downloads/chemistry-co2-lab.html','二氧化碳全景实验室.html')
    z.writestr('先读我.txt','解压后双击“二氧化碳全景实验室.html”，使用较新Chrome或Edge。下载后不需联网，不需安装软件。\n不要在压缩包内预览。浏览器须支持WebGL2。\n器材已搭好，无需自行组装。按高亮操作点完成七步实验，可切换八类易错示范与规范对照。\n操作步骤见README.md；模型为定性教学近似，器材是程序化临时资产。\n')
    for name in ['README.md','SCIENCE-AND-LIMITATIONS.md','TEST-REPORT.md']:
        z.write(root/'chemistry'/name,name)
    for p in sorted((root/'chemistry/evidence').glob('v2-*.png')):
        z.write(p,'实验截图/'+p.name)
print(out)
