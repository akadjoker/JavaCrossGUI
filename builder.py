import os
import subprocess
import time
import argparse
import zipfile
import shutil

ROOT = os.getcwd() + os.path.sep
#JAVA_HOME = "/usr/lib/jvm/java-17-openjdk-amd64"
#JAVA_HOME = ROOT + "jdk1.8.0_431"
JAVA_HOME = ROOT +"jdk-24"
JAVAC = os.path.join(JAVA_HOME, "bin", "javac")
JAVA = os.path.join(JAVA_HOME, "bin", "java")
ANDROID_SDK=ROOT +"sdks/android"
AAPT       =ANDROID_SDK+'/build-tools/34.0.0/aapt'
DX         =ANDROID_SDK+'/build-tools/34.0.0/dx'
DX8        =ANDROID_SDK+'/build-tools/34.0.0/d8'
ZIPALIGN   =ANDROID_SDK+'/build-tools/34.0.0/zipalign'
APKSIGNER  =ANDROID_SDK+'/build-tools/34.0.0/apksigner'
PLATFORM   =ANDROID_SDK+'/platforms/android-34/android.jar'
ANDROIDFXRT=ROOT+"/jarlibs/jfxrt.jar"
ANDROIDJFXDVK=ROOT+"/jarlibs/jfxdvk.jar"
ANDROIDFXCOMPACT=ROOT+"/jarlibs/compat-1.0.0.jar"
ANDROIDMULTIDEX=ROOT+"/jarlibs/android-support-multidex.jar"
ANDROIDDESUGAR=ROOT+"/jarlibs/desugar_jdk_libs-1.0.10.jar"
sep = ":" if os.name != "nt" else ";"




def clean(project_path):
    dirs_to_remove = [
        "tmp",
        "out",
        "dex",
        "dekstop",
    ]

    deleted = False
    for dir_name in dirs_to_remove:
        full_path = os.path.join(project_path, dir_name)
        if os.path.exists(full_path):
            shutil.rmtree(full_path)
            trace("🧹 Removido:", full_path)
            deleted = True

    # Remover chave gerada (ex: helloworld.key)
    app_name = os.path.basename(project_path.rstrip(os.path.sep))
    key_path = os.path.join(project_path, app_name + ".key")
    if os.path.exists(key_path):
        os.remove(key_path)
        trace("🧹 Removida a chave:", key_path)
        deleted = True

    if not deleted:
        trace("Nada para limpar.")
    else:
        trace("🧼 Clean completo.")




def trace(*args):
    if len(args) == 0:
        return
    print("[trace]", *args)

def runProcess(cmd, args):
    full_cmd = [cmd] + args
    process = subprocess.Popen(full_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = process.communicate()
    return process.returncode, out, err

def criar_manifesto_android(project_path, package_name, main_class):
    manifest_path = os.path.join(project_path, "AndroidManifest.xml")
    
    if os.path.exists(manifest_path):
        trace("AndroidManifest.xml já existe.")
        return

    trace("A criar AndroidManifest.xml por defeito...")

    xml_content = f'''<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package_name}" android:versionCode="1" android:versionName="1.0">
    <supports-screens android:xlargeScreens="true"/>
    <application android:label="Hello, Android" android:name="android.support.multidex.MultiDexApplication" android:debuggable="true">
        <activity android:name="javafxports.android.FXActivity" android:label="{main_class}" android:configChanges="orientation">
            <meta-data android:name="launcher.class" android:value="javafxports.android.DalvikLauncher"/>
            <!-- Full name of the application class to run -->
            <meta-data android:name="main.class" android:value="{package_name}.{main_class}"/>
            <!-- Jvm arguments (delimiter |) -->
            <meta-data android:name="jvm.args" android:value="-Djavafx.verbose=true|-Djavafx.name=value"/>
            <!-- Application arguments (delimiter |) -->
            <meta-data android:name="app.args" android:value="arg1|arg2"/>
            <!-- Jdwp debugging port. Don't forget to forward port (adb forward tcp:port1 tcp:port2) -->
            <meta-data android:name="debug.port" android:value="0"/>
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.INTERNET"/>
</manifest>'''

    with open(manifest_path, "w") as f:
        f.write(xml_content)
    
    trace("AndroidManifest.xml criado com sucesso.")


def CompileJavaDesktop(mainRoot,  appName,RUN):

    OSP=os.path.sep
    java = mainRoot+OSP+"src"
    tmp = mainRoot+OSP+"tmp"
    if not os.path.exists(tmp):
        trace("Create :"+tmp)
        os.mkdir(tmp)

    javaOut =mainRoot+OSP+"dekstop"
    if not os.path.exists(javaOut):
        trace("Create :"+javaOut)
        os.mkdir(javaOut)
        
    jumpCompile=False
    if not jumpCompile:  
        trace("Search java files ") 

        javaSrcFiles=[]
        for root, dirs, files in os.walk(java):
            for file in files:
                if file.endswith(".java"):
                    print(os.path.join(root, file))   
                    javaSrcFiles.append(os.path.join(root, file))

        javaSrcFiles.sort(reverse=True) 

        for src in javaSrcFiles:
            trace("Compile "+ src.strip())
            args=[]
            args.append("-nowarn")
            args.append("-Xlint:none")
            args.append("-J-Xmx2048m")
            args.append("-Xlint:unchecked")
                
            # args.append("-source")
            # args.append("1.8")
            # args.append("-target")  
            # args.append("1.8")

       

            
            args.append("-d")
            args.append(javaOut)
            args.append("-classpath")
            args.append("")
            args.append("-sourcepath")
            args.append(java+":"+javaOut)

            fxlib = os.path.join(ROOT, "javafx-sdk-24", "lib")
            args.append("--module-path")
            args.append(fxlib)
            args.append("--add-modules")
            args.append("javafx.controls,javafx.fxml,javafx.graphics,javafx.media,javafx.base,javafx.swing,javafx.web")
            args.append(src)

            src_modified_time = os.path.getmtime(src)
            src_convert_time = time.ctime(src_modified_time)

            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            maindir = os.path.dirname(os.path.abspath(src))
            maindir = maindir.replace("java","dekstop")
            objName=maindir+os.path.sep+basename_without_ext+".class"

            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    trace("Skip "+ src)
                    continue
            
            
            code, out, err=runProcess(JAVAC,args)
            if code!=0:
                trace("Error  compiling :"+err.decode("utf-8") )
                return False
            trace(out.decode("utf-8"))  
        
        trace('Java is compiled ...')

            
    # java --module-path /app/javafx-sdk-24/lib \
    #  --add-modules javafx.controls \
    #  -cp samples/SimpleGame/dekstop \
    #  com.djokersoft.simplegame.SimpleGame


    trace("Java compilado com sucesso.")
    if RUN:
        fxlib = os.path.join(ROOT, "javafx-sdk-24", "lib")
        args = [
            "--module-path", fxlib,
            "--add-modules", "javafx.controls,javafx.fxml,javafx.graphics,javafx.media,javafx.base,javafx.swing",
            "-cp", javaOut,
            appName   
        ]
        #args += ["-cp", javaOut, appName]

        code, out, err = runProcess(JAVA, args)
        if code != 0:
            trace("Erro ao correr:", out.decode("utf-8"))
            return False
        trace(out.decode("utf-8"))
    return True



def create_project(package_name, main_class):
    from pathlib import Path

    project_dir = ROOT + "samples/" + main_class
    src_path = os.path.join(project_dir, "src", *package_name.split('.'))
    os.makedirs(src_path, exist_ok=True)

    # Criar MainClass.java
    java_file = os.path.join(src_path, main_class + ".java")
    if not os.path.exists(java_file):
        with open(java_file, "w") as f:
            f.write(f"""package {package_name};

import javafx.application.Application;
import javafx.scene.Scene;
import javafx.scene.control.Label;
import javafx.stage.Stage;

public class {main_class} extends Application {{
    @Override
    public void start(Stage stage) {{
        Label label = new Label("Olá de {main_class}!");
        stage.setScene(new Scene(label, 300, 150));
        stage.setTitle("{main_class}");
        stage.show();
    }}

    public static void main(String[] args) {{
        launch(args);
    }}
}}
""")
        print(f"✅ Criado: {java_file}")

 
    res_path = os.path.join(project_dir, "icons", "mipmap")
    if not os.path.exists(res_path):
        shutil.copytree(ROOT + "androidFX/icons", os.path.join(project_dir, "res"))
        print("✅ Ícones default copiados.")

 
    manifest_path = os.path.join(project_dir, "AndroidManifest.xml")
    if not os.path.exists(manifest_path):
        manifest = f"""<?xml version="1.0" encoding="UTF-8"?>
<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package_name}" android:versionCode="1" android:versionName="1.0">
    <supports-screens android:xlargeScreens="true"/>
    <application android:label="{main_class}" android:name="android.support.multidex.MultiDexApplication" android:debuggable="true">
        <activity android:name="javafxports.android.FXActivity" android:label="{main_class}" android:configChanges="orientation">
            <meta-data android:name="launcher.class" android:value="javafxports.android.DalvikLauncher"/>
            <meta-data android:name="main.class" android:value="{package_name}.{main_class}"/>
            <meta-data android:name="jvm.args" android:value="-Djavafx.verbose=true|-Djavafx.name=value"/>
            <meta-data android:name="app.args" android:value="arg1|arg2"/>
            <meta-data android:name="debug.port" android:value="0"/>
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
    </application>
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"/>
    <uses-permission android:name="android.permission.INTERNET"/>
</manifest>
"""
        with open(manifest_path, "w") as f:
            f.write(manifest)
        print("✅ AndroidManifest.xml criado.")

    print(f"🎉 Projeto criado em: {project_dir}")


def CompileJavaFxAndroid(mainRoot,appName,ANDROID_PACK,ANDROID_ACTIVITY,NAME,RUN):


    OSP=os.path.sep
    

    
    java = mainRoot+OSP+"src"


    tmp = mainRoot+OSP+"tmp"
    if not os.path.exists(tmp):
        trace("Create :"+tmp)
        os.mkdir(tmp)

    javaOut =mainRoot+OSP+"out"
    if not os.path.exists(javaOut):
        trace("Create :"+javaOut)
        os.mkdir(javaOut)


    res = mainRoot+OSP+"res"
    default_res_path = os.path.join(ROOT, "androidFX", "icons")
    if not os.path.exists(res) or not any(os.scandir(res)):
        os.mkdir(res)
        trace("🖼️ Pasta 'res' não encontrada ou está vazia. A copiar os recursos default...")
        for dirpath, _, filenames in os.walk(default_res_path):
            for filename in filenames:
                src_file = os.path.join(dirpath, filename)
                relative = os.path.relpath(dirpath, default_res_path)
                dst_dir = os.path.join(res, relative)
                os.makedirs(dst_dir, exist_ok=True)
                dst_file = os.path.join(dst_dir, filename)
                shutil.copy2(src_file, dst_file)
                #trace(f"📥 Copiado: {src_file} → {dst_file}")
        

    dexFiles = mainRoot+OSP+"dex"+OSP
    if not os.path.exists(dexFiles):
        trace("Create :"+dexFiles)
        os.mkdir(dexFiles)

    assets = mainRoot+OSP+"assets"
    if not os.path.exists(assets):
        trace("Create :"+assets)
        os.mkdir(assets)

    

    debugKey=mainRoot+OSP+appName+".key"
    if not os.path.exists(debugKey):
        trace(" Generate "+debugKey+" keystor")
        args=[]
        args.append("-genkeypair")
        args.append("-validity")
        args.append("1000")  # mil anos???
        args.append("-dname")
        args.append("CN=djokersoft,O=Android,C=PT")
        args.append("-keystore")
        args.append(debugKey)
        args.append("-storepass")
        args.append("14781478")  #change pass
        args.append("-keypass")
        args.append("14781478")
        args.append("-alias")
        args.append("djokersoft")
        args.append("-keyalg")
        args.append("RSA")

        
        code, out, err=runProcess("keytool",args)
        if code!=0:
            trace("Error on generate keystore:"+err.decode("utf-8") )
            return False
        trace(out.decode("utf-8"))  


        

    manifFile = mainRoot+OSP+"AndroidManifest.xml"
    if not os.path.exists(manifFile):
        trace(" Generate "+manifFile)
        criar_manifesto_android(mainRoot, ANDROID_PACK, NAME)

    args=[]
    args.append("package")
    args.append("-f")
    args.append("-m")
    args.append("-J")
    args.append(java)
    args.append("-A")
    args.append(assets)

    args.append("-M")
    args.append(manifFile)
    args.append("-S")
    args.append(res)
    args.append("-I")
    args.append(PLATFORM)

    trace("Generate resources .")
    code, out, err=runProcess(AAPT,args)
    if code!=0:
        trace("Error on generate resources:"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8"))  

    jumpCompile=False
    if not jumpCompile:  
        trace("Search java files ") 

        javaSrcFiles=[]
        for root, dirs, files in os.walk(java):
            for file in files:
                if file.endswith(".java"):
                    print(os.path.join(root, file))   
                    javaSrcFiles.append(os.path.join(root, file))

        javaSrcFiles.sort(reverse=True) 

        for src in javaSrcFiles:
            trace("Compile "+ src.strip())
            args=[]
            args.append("-nowarn")
            args.append("-Xlint:none")
            args.append("-J-Xmx2048m")
            args.append("-Xlint:unchecked")
                
            args.append("-source")
            args.append("1.8")
            args.append("-target")  
            args.append("1.8")
            args.append("-d")
            args.append(javaOut)
            args.append("-classpath")
            args.append(ANDROIDFXRT+":"+ANDROIDJFXDVK+":"+PLATFORM+":"+javaOut)
            args.append("-sourcepath")
            args.append(java+":"+javaOut)
            args.append(src)

            src_modified_time = os.path.getmtime(src)
            src_convert_time = time.ctime(src_modified_time)

            filename, file_extension = os.path.splitext(src)
            basename = os.path.basename(src)
            basename_without_ext = os.path.splitext(os.path.basename(src))[0]
            maindir = os.path.dirname(os.path.abspath(src))
            maindir = maindir.replace("java","out")
            objName=maindir+os.path.sep+basename_without_ext+".class"

            if os.path.exists(objName):
                obj_modified_time = os.path.getmtime(objName)
                obj_convert_time = time.ctime(obj_modified_time)
                if (src_convert_time<obj_convert_time):
                    trace("Skip "+ src)
                    continue
            
            
            code, out, err=runProcess(JAVAC,args)
            if code!=0:
                trace("Error  compiling :"+err.decode("utf-8") )
                return False
            trace(out.decode("utf-8"))  
        
        trace('Java is compiled ...')

          
  


        trace("Translating in Dalvik bytecode...")

        javaClassFiles=[]
        for root, dirs, files in os.walk(javaOut):
            for file in files:
                if file.endswith(".class"):
                    javaClassFiles.append(os.path.join(root, file))

        args=[]
        args.append("--release")
        #args.append("--min-api")
        #args.append("21")
        args.append("--intermediate")
        args.append("--lib")
        args.append(PLATFORM)
        #args.append("--classpath")
        #args.append(JAVA_LIB_RT)

        for c in javaClassFiles:
            args.append(c)
        args.append("--output")
        args.append(dexFiles)
        code, out, err=runProcess(DX8,args)
        if code!=0:
            trace("Error  compiling :"+err.decode("utf-8") )
            return False
        trace(out.decode("utf-8"))

    


                 

    trace('Making APK...')

    args=[]
    args.append("package")
    args.append("-f")
    args.append("-m")
    args.append("-F")
    args.append(tmp+OSP+appName+".unaligned.apk")
    args.append("-M")
    args.append(manifFile)
    args.append("-S")
    args.append(res)
    args.append("-I")
    args.append(PLATFORM)
    
    
    code, out, err=runProcess(AAPT,args)
    if code!=0:
        trace("Error  packing apk :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8")) 

    trace("File is created in "+tmp+OSP+appName+".unaligned.apk")

    zip = zipfile.ZipFile(tmp+OSP+appName+".unaligned.apk",'a')

    dexListFiles=[]
    trace("look for dex files on ",dexFiles)
    for root, dirs, files in os.walk(dexFiles):
        for file in files:
            if file.endswith(".dex"):
                #print("DEX: ",os.path.join(root, file)," filename :",os.path.basename(file))   
                dexListFiles.append(os.path.join(root, file))
    
    
    for dex in dexListFiles:
        trace("Insert ", dex ," to "+os.path.basename(dex))
        zip.write(dex,os.path.basename(dex))
    

    
    javaFXPath=ROOT+os.path.sep+"androidFX/"
    jumpArm=False
    if not jumpArm:
        soListFiles=[]
        sharedFiles=javaFXPath+"lib/armeabi-v7a"
        #trace("look for shared files on ",sharedFiles)
        for root, dirs, files in os.walk(sharedFiles):
            for file in files:
                if file.endswith(".so"):
                    #print("dos: ",os.path.join(root, file)," filename :",os.path.basename(file))   
                    soListFiles.append(os.path.join(root, file))
        
        for so in soListFiles:
            #trace("Insert ", so ," to "+os.path.basename(so))
            zip.write(so,"lib/armeabi-v7a/"+os.path.basename(so))
    
    useArm64=False
    if useArm64:
        soListFiles=[]
        sharedFiles=javaFXPath+"lib/arm64-v8a"
        #trace("look for shared files on ",sharedFiles)
        for root, dirs, files in os.walk(sharedFiles):
            for file in files:
                if file.endswith(".so"):
                    #print("dos: ",os.path.join(root, file)," filename :",os.path.basename(file))   
                    soListFiles.append(os.path.join(root, file))
        
        for so in soListFiles:
            #trace("Insert ", so ," to "+os.path.basename(so))
            zip.write(so,"lib/arm64-v8a/"+os.path.basename(so))
    
    
    print("Add extra files")

    zip.write(javaFXPath+"javafx.platform.properties","assets/javafx.platform.properties")
    zip.write(javaFXPath+"javafx.properties","assets/javafx.properties")

    print("Add dex files")
    zip.write(javaFXPath+"dex"+OSP+"classes2.dex","classes2.dex")
    zip.write(javaFXPath+"dex"+OSP+"classes3.dex","classes3.dex")
    zip.write(javaFXPath+"dex"+OSP+"classes4.dex","classes4.dex")
    zip.write(javaFXPath+"dex"+OSP+"classes5.dex","classes5.dex")
    zip.write(javaFXPath+"dex"+OSP+"classes6.dex","classes6.dex")
    
    extraFiles=javaFXPath+"extra"
    assetsListFiles=[]
    for root, dirs, files in os.walk(extraFiles):
        for file in files:
                assetsListFiles.append(os.path.join(root, file))
    
    for extra in assetsListFiles:
        newName=extra.replace(extraFiles,"")
        #trace("Insert ", extra ," to "+newName)
        zip.write(extra,newName)

    zip.close()

    appSigned = mainRoot+OSP+appName+".signed.apk"
    trace("Sign app ")
    args=[]
    args.append("sign")
    args.append("--ks")
    args.append(debugKey)
    args.append("--ks-key-alias")
    args.append("djokersoft")
    args.append("--ks-pass")
    args.append("pass:14781478")
    args.append("--in")
    args.append(tmp+OSP+appName+".unaligned.apk")
    args.append("--out")
    args.append(appSigned)
    
    
    
    code, out, err=runProcess(APKSIGNER,args)
    if code!=0:
        trace("Error  packing apk :"+err.decode("utf-8") )
        return False
    trace(out.decode("utf-8")) 
    trace("Build competed ;D ")
    if RUN:
        trace("Try stop  "+ANDROID_PACK+"...")
        args=[]
        args.append("shell")
        args.append("am")
        args.append("force-stop")
        args.append(ANDROID_PACK+"/"+ANDROID_ACTIVITY)
        code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
        if code!=0:
            trace("Error  stoping  apk :"+err.decode("utf-8") )
        trace(out.decode("utf-8")) 

        trace('Try remove app ...')
        args=[]
        args.append("uninstall")
        args.append(ANDROID_PACK)
        code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
        if code!=0:
            trace("Error  uninstall  apk :"+err.decode("utf-8") )
        trace(out.decode("utf-8")) 

        trace('Try install app ...')
        args=[]
        args.append("install")
        args.append("-r")
        args.append(appSigned)
        code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
        if code!=0:
            trace("Error  installing  apk :"+err.decode("utf-8") )
            
        trace(out.decode("utf-8")) 

        trace('Try run app ...')
        args=[]
        args.append("shell")
        args.append("am")
        args.append("start")
        args.append("-n")
        args.append(ANDROID_PACK+"/"+ANDROID_ACTIVITY)
        
        code, out, err=runProcess(ANDROID_SDK+"/platform-tools/adb",args)
        if code!=0:
            trace("Error  running  apk :"+err.decode("utf-8") )
            return False
        trace(out.decode("utf-8")) 
    return True


# print(JAVA_HOME)



# args = ["-version"]


# code, out, err = runProcess(JAVA, args)
# if code != 0:
#     trace("Erro ao correr java:", err.decode("utf-8"))
# else:
#     trace( err.decode("utf-8"))  # 


# code, out, err = runProcess(JAVAC, args)
# if code != 0:
#     trace("Erro ao correr javac:", err.decode("utf-8"))
# else:
#     trace(  err.decode("utf-8"))  

# CompileJavaDesktop(
#     mainRoot=ROOT+"samples/HelloFX", 
#     appName="HelloFX", 
#     srcFolder="src", 
#     javaSrcFiles=["HelloFX.java"]
# )

# CompileJavaDesktop(
#     mainRoot=ROOT+"samples/tutorial", 
#     appName="HelloWorld", 
#     srcFolder="src", 
#     javaSrcFiles=["HelloWorld.java"]
# )


# CompileJavaDesktop(
#     mainRoot=ROOT+"samples/calculadora", 
#     appName="Calculadora", 
#     srcFolder="src", 
#     javaSrcFiles=["Calculadora.java"]
# )

# CompileJavaDesktop(
#     mainRoot=ROOT+"samples/tutorial", 
#     appName="HelloAndroid", 
#     srcFolder="src", 
#     javaSrcFiles=["HelloAndroid.java"]
# )


#CompileJavaFxAndroid( ROOT+"samples/HelloWorld", "helloworld", "org.javafxports.helloworld", "javafxports.android.FXActivity")


# def main():
#     parser = argparse.ArgumentParser(
#         description="Sistema de build JavaFX - Android & Desktop"
#     )
#     parser.add_argument("--create", nargs=2, metavar=("package", "MainClass"), help="Criar novo projeto")

#     parser.add_argument("project", help="Diretório do projeto (raiz)")
#     parser.add_argument("package", help="Nome do package Java (ex: org.exemplo.app)")

    
#     parser.add_argument(
#         "--target", 
#         choices=["android", "desktop"], 
#         default="desktop",
#         help="Tipo de build (android ou desktop)"
#     )

#     parser.add_argument(
#         "--name",
#         type=str,
#         default="Main",
#         help="Nome da classe principal (Main class)"
#     )
#     parser.add_argument(
#         "--clean",
#         action="store_true",
#         help="Limpa todos os ficheiros gerados pelo sistema de build"
#     )

#     args = parser.parse_args()

#     project_path = args.project
#     package_name = args.package
#     build_type = args.target
#     main_class = "Main"

#     if args.name:
#         main_class = args.name
    
#     if args.clean:
#         print(f"🧹 A limpar {project_path} ...")
#         clean(project_path)
#         return
    

#     app_name = os.path.basename(project_path.rstrip(os.path.sep))

#     if build_type == "android":
#         print(f"📱 A compilar {app_name} para Android...")
#         CompileJavaFxAndroid(
#             mainRoot=project_path,
#             appName=app_name,
#             ANDROID_PACK=package_name,
#             ANDROID_ACTIVITY="javafxports.android.FXActivity",
#             NAME = main_class
#         )

#     elif build_type == "desktop":
#         print(f"🖥️  A compilar {app_name} para Desktop...")
#         CompileJavaDesktop(
#             mainRoot=project_path,
#             appName=package_name + "." + main_class
#         )

# # Desktop build:
# # python3 builder.py samples/HelloWorld org.javafxports.helloworld --target desktop

# # Android build:
# # python3 builder.py samples/HelloWorld org.javafxports.helloworld --target android



# # CompileJavaDesktop(
# #     mainRoot="samples/HelloWorld", 
# #     appName="org.javafxports.helloworld.HelloAndroid"
# # )



def main():
    parser = argparse.ArgumentParser(
        description="Sistema de build JavaFX - Android & Desktop"
    )

    parser.add_argument("project", nargs="?", help="Diretório do projeto (raiz)")
    parser.add_argument("package", nargs="?", help="Nome do package Java (ex: org.exemplo.app)")
    parser.add_argument(    "--run",action="store_true",
    help="Corre a app depois de compilar (desktop ou android)"
)

    parser.add_argument(
        "--target", 
        choices=["android", "desktop"], 
        default="desktop",
        help="Tipo de build (android ou desktop)"
    )
    parser.add_argument(
        "--name",
        help="Nome da class Main"
    )
    parser.add_argument(
        "--create", nargs=2, metavar=("package", "MainClass"),
        help="Cria um novo projeto base com JavaFX"
    )
    parser.add_argument(
        "--clean", action="store_true",
        help="Limpa pastas temporárias e binários gerados"
    )
    args = parser.parse_args()


    if args.create:
        package_name, main_class = args.create
        create_project(package_name, main_class)
        return

    if not args.project or not args.package:
        print("Erro: tens de indicar o caminho do projeto e o package.")
        print("Exemplo: python3 builder.py samples/HelloWorld org.exemplo.app --target desktop")
        return

    run = args.run
    project_path = args.project
    package_name = args.package
    build_type = args.target
    main_class = args.name if args.name else "Main"
    app_name = os.path.basename(project_path.rstrip(os.path.sep))

    if args.clean:
        print(f"🧹 A limpar projeto {app_name}...")
        for folder in ["out", "tmp", "dex", "assets", "dekstop"]:
            path = os.path.join(project_path, folder)
            if os.path.exists(path):
                shutil.rmtree(path)
                print(f"  🗑️  Removido: {folder}")
        return

    if build_type == "android":
        print(f"📱 A compilar {app_name} para Android...")
        CompileJavaFxAndroid(
            mainRoot=project_path,
            appName=app_name,
            ANDROID_PACK=package_name,
            ANDROID_ACTIVITY="javafxports.android.FXActivity",
            NAME = main_class,
            RUN = run
        )

    elif build_type == "desktop":
        print(f"🖥️  A compilar {app_name} para Desktop...")
        full_class_name = package_name + "." + main_class
        CompileJavaDesktop(
            mainRoot=project_path,
            appName=full_class_name, RUN = run
        )

if __name__ == "__main__":
    main()
