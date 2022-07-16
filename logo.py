from manim import *
import math
import itertools

def lerp(a, b, t):
    return (1.0 - t)*a + t*b

def smlerp(a,b,t):
    x = t * t * (3 - 2 * t)
    return (1.0 - x)*a + x*b

class BooleanOperations(Scene):
    def construct(self):
        self.filter_rot = 0

        def updateFilters(mob, dt):
            # What is calling this initially to populate mobject? this is shit
            if self.filter_rot == 0:
                self.filter_rot += dt
                return

            mob.submobjects = []
            start_angle = 0
            end_angle = PI/2
            n_filters = 5
            filter_angles = []
            circles = []

            for i in range(1,n_filters+1):
                filter_angles.append(start_angle + i*(end_angle - start_angle)/(n_filters+1))
                angle = smlerp(0, 2*PI*(i-1)/n_filters, self.filter_rot)
                circle = Circle(radius=1.0, arc_center=0.5*math.cos(angle)*RIGHT + 0.5*math.sin(angle)*UP)

                circles.append(circle)
            for i in range(1, n_filters+1):
                for intersects in itertools.combinations(range(n_filters), i):
                    # Apply malus's law
                    intensity = 1.0 # unpolarised initially
                    p_angle = start_angle 
                    for j in intersects:
                        dAngle = filter_angles[j] - p_angle
                        intensity *= math.pow(math.cos(dAngle), 2)
                        p_angle = filter_angles[j]
                    intensity *= math.pow(math.cos(end_angle - p_angle), 2)

                    if i == n_filters:
                        mob.add(Intersection(*circles, color=WHITE, fill_opacity=intensity))
                    else:
                        intersect_circles = [circles[j] for j in range(n_filters) if j in intersects]
                        if len(intersect_circles) == 1:
                            intersect = intersect_circles[0]
                        else:
                            intersect = Intersection(*intersect_circles)
                        not_intersect_circles = [circles[j] for j in range(n_filters) if j not in intersects]
                        if len(not_intersect_circles) == 1:
                            not_intersect = not_intersect_circles[0]
                        else:
                            not_intersect = Union(*not_intersect_circles)

                        mob.add(Difference(intersect, not_intersect, color=WHITE, fill_opacity=intensity))
            self.filter_rot += dt
            self.filter_rot = min(self.filter_rot,1.0)

        filters = Mobject().add_updater(updateFilters, call_updater=False)
        self.add(filters)
        self.wait(2.0)
