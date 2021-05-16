% testing code for nlos detection with toolbox geom3d

% help functions: detect_los, getBox
clear; clc;
% anchor, tag positions
anchor = [-1.5, 0.0, 1.5;
           1.5, 0.0, 1.25];

tag = [1.0, -2.5, 1.0];

% define obstacles
obs1_center = [0.0, -1.5, 0.4]; % center
obs1_lwd = [0.3, 0.3, 2*obs1_center(3)];      % the total lengths of the x,y,z axes (length, wideth, depth)

obs2_center = [1.3, -1.0, 0.85]; % center
obs2_lwd = [0.3, 0.3, 2*obs2_center(3)];      

obs3_center = [0.5, 0.0, 0.75]; % center
obs3_lwd = [0.3, 0.3, 2*obs3_center(3)];     

% compute the box = [x_min, x_max, y_min, y_max, z_min, z_max] for nlos detection

box1 = getBox(obs1_center, obs1_lwd);
box2 = getBox(obs2_center, obs2_lwd);
box3 = getBox(obs3_center, obs3_lwd);

an1_tag_edge = [anchor(1,:), tag];     % get the segment line (edge) (x1,y1,z1,x2,y2,z2)
an2_tag_edge = [anchor(2,:), tag];
an1_an2_edge = [anchor(1,:), anchor(2,:)];

% detect los
Edge = [an1_tag_edge;
        an2_tag_edge;
        an1_an2_edge ];
Box =  [box1;
        box2;
        box3];

% LOS is a matrix with LOS(i,j) indicates the los condition of Edge(i,:)
% and Box(j,:)
for i=1:3
    for j=1:3
        LOS(i,j) = detect_los(Edge(i,:), Box(j,:));
    end
end


%% visualization
figure('Renderer', 'painters', 'Position', [10 10 1080 860]);
Dis = 0.05;
% plot anchor and tags
scatter3(anchor(:,1), anchor(:,2), anchor(:,3),'filled','MarkerFaceColor',[1 0 0])
hold on
scatter3(tag(1),tag(2),tag(3),'filled','MarkerFaceColor',[0 0 1])
hold on
text(anchor(1,1)+Dis, anchor(1,2)+Dis, anchor(1,3)+Dis, ['anchor1'], 'HorizontalAlignment','left','Interpreter','latex','FontSize',16);
hold on
text(anchor(2,1)+Dis, anchor(2,2)+Dis, anchor(2,3)+Dis, ['anchor2'], 'HorizontalAlignment','left','Interpreter','latex','FontSize',16);
hold on
text(tag(1)+Dis,      tag(2)+Dis,      tag(3)+Dis,      ['tag'],     'HorizontalAlignment','left','Interpreter','latex','FontSize',16);
hold on 
% plot obstacles
cub1=drawCuboid([obs1_center   obs1_lwd    0 0 0], 'FaceColor', 'b','FaceAlpha',.3);
hold on
cub2=drawCuboid([obs2_center   obs2_lwd    0 0 0], 'FaceColor', [0.8500, 0.3250, 0.0980],'FaceAlpha',.3);
hold on
cub3=drawCuboid([obs3_center   obs3_lwd    0 0 0], 'FaceColor', [0.5, 1.0, 0.83],'FaceAlpha',.3);
view(20,25)
hold on

% plot communication line
plot3(anchor(:,1), anchor(:,2), anchor(:,3))
plot3([anchor(1,1) tag(1)], [anchor(1,2) tag(2)], [anchor(1,3) tag(3)])
plot3([anchor(2,1) tag(1)], [anchor(2,2) tag(2)], [anchor(2,3) tag(3)])

% view(-30,10)
xlim([-3.5, 3.5]);
ylim([-4.0, 4.0]);
zlim([-0.5, 3.5]);
xlabel('$x$ axis [m]','Interpreter','latex','Fontsize',24)
ylabel('$y$ axis [m]','Interpreter','latex','Fontsize',24)
zlabel('$z$ axis [m]','Interpreter','latex','Fontsize',24)
grid on



