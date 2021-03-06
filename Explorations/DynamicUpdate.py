import matplotlib.pyplot as plt
class DynamicUpdate():
    #Suppose we know the x range
    #plt.subplot(1, 2, 1)
    def on_launch(self):
        #Set up plot
        
        self.figure, self.ax = plt.subplots()
        self.figure.set_figheight(15)
        self.figure.set_figwidth(25)

        self.lines, = self.ax.plot([],[])
        #Autoscale on unknown axis and known lims on the other
        self.ax.set_autoscaley_on(True)
        #Other stuff
        self.ax.grid()

    def on_running(self, xdata, ydata):
        #Update data (with the new _and_ the old points)
        self.lines.set_xdata(xdata)
        self.lines.set_ydata(ydata)
        #Need both of these in order to rescale
        self.ax.relim()
        self.ax.autoscale_view()
        #We need to draw *and* flush
        self.figure.canvas.draw()
        self.figure.canvas.flush_events()
