from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        
        self.no_flights=len(flights)
        self.no_cities=self.no_of_cities(flights, self.no_flights)
        self.flight_graph=Graph(self.no_cities)
        for i in range(len(flights)):
            self.flight_graph.add_edge(flights[i].start_city, flights[i].end_city, flights[i])
        pass
    

    def no_of_cities(self, flights, n):
        max_city_index = -1
        for flight in flights:
            max_city_index = max(max_city_index, flight.start_city, flight.end_city)
        return max_city_index + 1  # +1 to include the last city index

    
    # you have changed it to earliest!!!!!!!!!!!!!!!!!

    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        arrives the earliest
        """
        # if start_city==end_city:
        #     ??
        # else:
        # queue ke resizing ke karan time complexity
        # agr t1,t2 na follow kiya fir kya

        q=Queue(self.no_flights)
        par=[None]*(self.no_cities)
        dist = [float('inf')] * (self.no_cities)
        earliest_time=float('inf')
        flight=Flight(-1,0,0,0,0,0)
        q.enqueue((start_city, flight))
        dist[start_city]=0
        par[start_city]=flight  
        while(not q.is_empty()):
            new=q.dequeu()
            recent=new[0]
            if recent==end_city:
                earliest_time=min(earliest_time, new[1].arrival_time)
                if earliest_time==new[1].arrival_time:
                    par[end_city]=new[1]
                continue
            else:
                # if recent < len(self.flight_graph.adj_list) and self.flight_graph.adj_list[recent]:
                    for i in range(len(self.flight_graph.adj_list[recent])):
                        neighbour=self.flight_graph.adj_list[recent][i]
                        if neighbour[1].departure_time >=t1 and neighbour[1].arrival_time <=t2:
                            if par[recent].flight_no >= 0:
                                x=20
                            else:
                                x=0
                            if neighbour[1].departure_time>=x+par[recent].arrival_time:
                                if dist[neighbour[0]]== float('inf'):
                                    dist[neighbour[0]]=dist[recent]+1
                                    par[neighbour[0]]=neighbour[1]
                                    q.enqueue(neighbour)
                                elif dist[neighbour[0]]==dist[recent] + 1 :
                                    if par[neighbour[0]].arrival_time > neighbour[1].arrival_time:
                                        par[neighbour[0]]=neighbour[1]
                                        q.enqueue(neighbour) 
         
        if par[end_city] is None:
            return []
        else:
            curr=end_city
            final=[]
            while(par[curr].flight_no >= 0):
                final.append(par[curr])
                curr=par[curr].start_city
            final_final=[]
            for i in range(len(final) - 1, -1, -1):
                final_final.append(final[i])
            return final_final
        pass
    
    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route is a cheapest route
        """
        q=MinHeap()
        dist = [float('inf')] * (self.no_flights+1)
        par=[None]*(self.no_flights+1)
        answer=None
        for i in range(len(self.flight_graph.adj_list[start_city])):
            neighbour=self.flight_graph.adj_list[start_city][i]
            if neighbour[1].departure_time>=t1 and neighbour[1].arrival_time<=t2:
                dist[neighbour[1].flight_no]=neighbour[1].fare
                par[neighbour[1].flight_no]=None
                q.heap_push((neighbour[1].fare, neighbour[1]))
        cheapest=float('inf')
        while ( not q.is_empty()):
            new=q.heap_pop()
            if new[1].end_city==end_city:
                cheapest=min(cheapest, new[0])
                if cheapest==new[0]:
                    answer=new[1]
                continue
            for i in range(len(self.flight_graph.adj_list[new[1].end_city])):
                neighbour=self.flight_graph.adj_list[new[1].end_city][i]
                if neighbour[1].departure_time >=t1 and neighbour[1].arrival_time <= t2:
                    if neighbour[1].departure_time>=20+new[1].arrival_time:
                        distance=new[0]+neighbour[1].fare
                        if distance < dist[neighbour[1].flight_no]:
                            # print(distance)
                            dist[neighbour[1].flight_no]=distance
                            par[neighbour[1].flight_no]=new[1]
                            q.heap_push((distance, neighbour[1]))
        if answer is None:
            return []
        # elif par[answer.flight_no] is None:
        #     return []
        else:
            curr=answer
            final=[]
            # final.append(answer)
            while(curr):
                final.append(curr)
                curr=par[curr.flight_no]
            final_final=[]
            for i in range(len(final) - 1, -1, -1):
                final_final.append(final[i])
            return final_final
        pass
        
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        
        q=MinHeap2()
        cost = [float('inf')] * (self.no_flights)
        dist = [float('inf')] * (self.no_flights)
        # lev=[float('inf')*(self.no_flights)]
        par=[None]*(self.no_flights)
        answer=None
        for i in range(len(self.flight_graph.adj_list[start_city])):
            neighbour=self.flight_graph.adj_list[start_city][i]
            if neighbour[1].departure_time>=t1 and neighbour[1].arrival_time<=t2:
                cost[neighbour[1].flight_no]=neighbour[1].fare
                dist[neighbour[1].flight_no]=0
                par[neighbour[1].flight_no]=None
                q.heap_push((cost[neighbour[1].flight_no], neighbour[1], dist[neighbour[1].flight_no] ))
        cheapest=float('inf')
        lev=float('inf')
        while ( not q.is_empty()):
            new=q.heap_pop()
            # if new[1].end_city==3:
            #     if(new[1].flight_no == 5):
                    # print(cost[new[1].flight_no])
            if new[1].end_city==end_city:
                # print("yo")
                # print(new[1].end_city)
                # print(new[1].flight_no)
                if (new[2]<lev or (new[2]==lev and new[0]<cheapest)):
                # print(cheapest)
                # if cheapest==new[0]:
                    answer=new[1]
                    cheapest=new[0]
                    lev=new[2]
                continue
            for i in range(len(self.flight_graph.adj_list[new[1].end_city])):
                neighbour=self.flight_graph.adj_list[new[1].end_city][i]
                if neighbour[1].departure_time >=t1 and neighbour[1].arrival_time <= t2:
                    if neighbour[1].departure_time>=20+new[1].arrival_time:
                        # if new[1].flight_no==5:
                            # print("reached")
                            # print(neighbour[1].flight_no)
                            # print("hi")
                            # print(cost[neighbour[1].flight_no])
                        if dist[neighbour[1].flight_no]== float('inf'):
                            dist[neighbour[1].flight_no]=dist[new[1].flight_no]+1
                            cost[neighbour[1].flight_no]=cost[new[1].flight_no]+neighbour[1].fare
                            par[neighbour[1].flight_no]=new[1]
                            q.heap_push((cost[neighbour[1].flight_no],neighbour[1], dist[neighbour[1].flight_no] ))
                        
        if answer is None:
            return []
        # elif par[answer.flight_no] is None:
        #     return []
        else:
            curr=answer
            final=[]
            # final.append(answer)
            while(curr):
                final.append(curr)
                curr=par[curr.flight_no]
            final_final=[]
            for i in range(len(final) - 1, -1, -1):
                final_final.append(final[i])
            return final_final
        
        pass
        

class Graph:
    def __init__(self, no_cities):
        self.adj_list=[[] for i in range(no_cities)]
        pass
    def add_edge(self, city1, city2, flight):
        self.adj_list[city1].append((city2,flight))

class Queue:
    def __init__(self, capacity):
        self.capacity = capacity
        self.queue=[None] * capacity
        self.front=0
        self.rear=0
        self.size=0

    def enqueue(self, item):
        if self.size==self.capacity:
            return False
        self.queue[self.rear] = item
        self.rear=(self.rear+1)%self.capacity
        self.size+= 1
        return True

    def dequeu(self):
        if self.size == 0:
            return None
        item = self.queue[self.front]
        self.front = (self.front+1) % self.capacity
        self.size -= 1
        return item

    def is_empty(self):
        return self.size == 0

class MinHeap:
    def __init__(self):
        self.heap = []

    def heap_push(self,item):
        self.heap.append(item)
        self.sift_up(len(self.heap)-1)

    def heap_pop(self):
        if not self.heap:
            return None
        self.heap[0], self.heap[len(self.heap)-1] = self.heap[len(self.heap)-1], self.heap[0]
        min_item = self.heap.pop()
        self.sift_down(0)
        return min_item

    def sift_up(self, index):
        parent = (index - 1) // 2
        while index > 0 and self.heap[index][0] < self.heap[parent][0]:
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def sift_down(self,index):
        while 2*index+1 < len(self.heap):
            left=2*index+1
            right=left+1
            smallest=left
            if right<len(self.heap) and self.heap[right][0]<self.heap[left][0]:
                smallest =right
            if self.heap[smallest][0] < self.heap[index][0]:
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def is_empty(self):
        return len(self.heap) == 0
    
class MinHeap2:
    def __init__(self):
        self.heap = []

    def heap_push(self, item):
        # Add the new item to the end of the heap
        self.heap.append(item)
        # Move the new item up to restore the heap property
        self.sift_up(len(self.heap) - 1)

    def heap_pop(self):
        if not self.heap:
            return None
        self.heap[0], self.heap[len(self.heap) - 1] = self.heap[len(self.heap) - 1], self.heap[0]
        min_item = self.heap.pop()
        self.sift_down(0)
        return min_item

    def sift_up(self, index):
        parent = (index - 1) // 2
        # Move up while the current item is smaller than its parent
        while index > 0 and (self.heap[index][2] < self.heap[parent][2] or (self.heap[index][2]==self.heap[parent][2] and self.heap[index][0]<self.heap[parent][0])):
            self.heap[index], self.heap[parent] = self.heap[parent], self.heap[index]
            index = parent
            parent = (index - 1) // 2

    def sift_down(self, index):
        while 2 * index + 1 < len(self.heap):
            left = 2 * index + 1
            right = left + 1
            smallest = left
            if right < len(self.heap):
                if(self.heap[right][2] < self.heap[left][2] or (self.heap[right][2]==self.heap[left][2] and self.heap[right][0]<self.heap[left][0])):
                    smallest = right
            # if self.heap[smallest][0] < self.heap[index][0]:/
            if (self.heap[smallest][2] < self.heap[index][2] or (self.heap[smallest][2]==self.heap[index][2] and self.heap[smallest][0]<self.heap[index][0])):
                self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
                index = smallest
            else:
                break

    def is_empty(self):
        return len(self.heap) == 0
