"""Install free offline translation packages once. No account or API key."""
import argostranslate.package as packages
packages.update_package_index()
available=packages.get_available_packages()
installed={(p.from_code,p.to_code) for p in packages.get_installed_packages()}
for source,target in [('zh','en'),('en','pt')]:
    if (source,target) not in installed:
        model=next(p for p in available if p.from_code==source and p.to_code==target)
        print('Baixando modelo',source,target,flush=True)
        packages.install_from_path(model.download())
        print('Instalado',source,target,flush=True)
print('Modelos prontos.',flush=True)
