from worker_automate_hub.tasks.jobs.fazer_pudim import fazer_pudim
from worker_automate_hub.tasks.jobs.login_emsys import login_emsys

task_definitions = {
    "5b295021-8df7-40a1-a45e-fe7109ae3902": fazer_pudim,
    "a0788650-de48-454f-acbf-3537ead2d8ed": login_emsys,
}
