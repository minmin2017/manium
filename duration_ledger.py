import ast
import os
import sys

def analyze_scene_duration(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        source = f.read()

    tree = ast.parse(source, filename=file_path)
    scene_durations = {}

    for node in tree.body:
        if isinstance(node, ast.ClassDef):
            class_name = node.name
            total_duration = 0.0
            events = []

            for item in node.body:
                if isinstance(item, ast.FunctionDef) and item.name == "construct":
                    for stmt in ast.walk(item):
                        if isinstance(stmt, ast.Call):
                            # check self.play(...)
                            if isinstance(stmt.func, ast.Attribute) and stmt.func.attr == "play":
                                run_time = 1.0 # manim default
                                for kw in stmt.keywords:
                                    if kw.arg == "run_time":
                                        if isinstance(kw.value, ast.Constant):
                                            run_time = float(kw.value.value)
                                total_duration += run_time
                                events.append(("play", run_time))

                            # check self.wait(...)
                            elif isinstance(stmt.func, ast.Attribute) and stmt.func.attr == "wait":
                                wait_time = 1.0 # manim default
                                if stmt.args:
                                    arg = stmt.args[0]
                                    if isinstance(arg, ast.Constant):
                                        wait_time = float(arg.value)
                                total_duration += wait_time
                                events.append(("wait", wait_time))

                            # check self.fade_out_all(...)
                            elif isinstance(stmt.func, ast.Attribute) and stmt.func.attr == "fade_out_all":
                                run_time = 0.8
                                for kw in stmt.keywords:
                                    if kw.arg == "run_time":
                                        if isinstance(kw.value, ast.Constant):
                                            run_time = float(kw.value.value)
                                total_duration += run_time
                                events.append(("fade_out_all", run_time))

            if events:
                scene_durations[class_name] = (total_duration, events)

    return scene_durations

def main():
    files = [
        "double_slit_01_intro_wave.py",
        "double_slit_02_apparatus_paths.py",
        "double_slit_03_geometry_spacing.py",
        "double_slit_04_lab_real.py",
    ]
    grand_total = 0.0
    print(f"{'Scene':<25} | {'Duration (s)':<12} | {'Events count'}")
    print("-" * 50)
    for fname in files:
        if os.path.exists(fname):
            durs = analyze_scene_duration(fname)
            for cls, (dur, evts) in durs.items():
                print(f"{cls:<25} | {dur:<12.2f} | {len(evts)}")
                grand_total += dur
    print("-" * 50)
    print(f"Grand Total: {grand_total:.2f}s ({grand_total/60:.2f} min)")

if __name__ == "__main__":
    main()
