import DaVinciResolveScript as dvr
import time

def set_timeline_name_to_project_name():
    resolve = dvr.scriptapp("Resolve")
    project_manager = resolve.GetProjectManager()
    project = project_manager.GetCurrentProject()

    if project:
        project_name = project.GetName()
        current_timeline = project.GetCurrentTimeline()

        if current_timeline:
            current_timeline_name = current_timeline.GetName()
            if current_timeline_name != project_name:
                current_timeline.SetName(project_name)
                print(f"Timeline name set to project name: {project_name}")
        else:
            print("No timeline found.")
    else:
        print("No project found.")

if __name__ == "__main__":
    last_timeline_name = None
    while True:
        resolve = dvr.scriptapp("Resolve")
        project_manager = resolve.GetProjectManager()
        project = project_manager.GetCurrentProject()

        if project:
            current_timeline = project.GetCurrentTimeline()
            if current_timeline:
                current_timeline_name = current_timeline.GetName()
                if current_timeline_name != last_timeline_name:
                    set_timeline_name_to_project_name()
                    last_timeline_name = current_timeline_name
        time.sleep(5)  # 5초마다 상태 확인
