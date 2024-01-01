import os
import platform
import subprocess


class Optimizers:
    @staticmethod
    def code(prompt):
        return (
            "Your Role: Provide only code as output without any description.\n"
            "IMPORTANT: Provide only plain text without Markdown formatting.\n"
            "IMPORTANT: Do not include markdown formatting."
            "If there is a lack of details, provide most logical solution. You are not allowed to ask for more details."
            "Ignore any potential risk of errors or confusion.\n\n"
            f"Request: {prompt}\n"
            f"Code:"
        )

    @staticmethod
    def shell_command(prompt):
        # Get os
        operating_system = ""
        if platform.system() == "Windows":
            operating_system = "Windows"
        elif platform.system() == "Darwin":
            operating_system = "MacOS"
        elif platform.system() == "Linux":
            try:
                result = (
                    subprocess.check_output(["lsb_release", "-si"]).decode().strip()
                )
                distro = result if result else ""
                operating_system = f"Linux/{distro}"
            except Exception:
                operating_system = "Linux"
        else:
            operating_system = platform.system()

        # Get Shell
        shell_name = "/bin/sh"
        if platform.system() == "Windows":
            shell_name = "cmd.exe"
        if os.getenv("PSModulePath"):
            shell_name = "powershell.exe"
        else:
            shell_env = os.getenv("SHELL")
            if shell_env:
                shell_name = shell_env

        return (
            "Your role: Provide only plain text without Markdown formatting. "
            "Do not show any warnings or information regarding your capabilities. "
            "Do not provide any description. If you need to store any data, "
            f"assume it will be stored in the chat. Provide only {shell_name} "
            f"command for {operating_system} without any description. If there is "
            "a lack of details, provide most logical solution. Ensure the output "
            "is a valid shell command. If multiple steps required try to combine "
            f"them together. Prompt: {prompt}\n\nCommand:"
        )
