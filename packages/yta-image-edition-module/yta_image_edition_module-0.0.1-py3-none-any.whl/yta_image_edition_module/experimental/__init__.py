from subprocess import run

# TODO: Move this method, this is video related, not image
def remove_background_video(video_filename, output_filename):
    # TODO: Move to 'video_utils'
    # TODO: This is too demanding as I cannot process it properly
    # Output must end in .mov to preserve transparency
    # TODO: Refactor this code to make it work with python code and not command
    command_parameters = ['backgroundremover', '-i', video_filename, '-tv', '-o', output_filename]

    run(command_parameters)
